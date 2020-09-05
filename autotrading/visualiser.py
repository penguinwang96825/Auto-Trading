import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.utils import class_weight
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from ml_backtest import generate_feature
from ml_backtest import triple_barrier


def run_models_exps(X_train, y_train, X_test, y_test, print_result=False, plot=True):
    '''
    Args:
        X_train (:obj: pd.DataFrame):
        y_train (:obj: pd.DataFrame):
        X_test (:obj: pd.DataFrame):
        y_test (:obj: pd.DataFrame):
        print_result (:obj: bool):
        plot (:obj: bool):

    Returns:
        :obj: pd.DataFrame, pd.DataFrame
            DataFrame objects for models result.
    '''

    dfs = []
    models = [
              ('LogReg', LogisticRegression()),
              ('RF', RandomForestClassifier()),
              ('KNN', KNeighborsClassifier()),
              ('SVM', SVC()),
              ('GNB', GaussianNB()),
              ('XGB', XGBClassifier())
            ]
    results = []
    names = []
    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    target_names = ['SELL', 'BUY']
    for name, model in tqdm(models):
        kfold = model_selection.KFold(n_splits=5, shuffle=False, random_state=1016)
        cv_results = model_selection.cross_validate(model, X_train, y_train, cv=kfold, scoring=scoring)
        clf = model.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        if print_result:
            print(name)
            print(classification_report(y_test, y_pred, target_names=target_names))
        results.append(cv_results)
        names.append(name)
        this_df = pd.DataFrame(cv_results)
        this_df['model'] = name
        dfs.append(this_df)
        final = pd.concat(dfs, ignore_index=True)

    bootstraps = []
    for model in list(set(final.model.values)):
        model_df = final.loc[final.model == model]
        bootstrap = model_df.sample(n=30, replace=True)
        bootstraps.append(bootstrap)

    bootstrap_df = pd.concat(bootstraps, ignore_index=True)
    results_long = pd.melt(bootstrap_df, id_vars=['model'], var_name='metrics', value_name='values')
    time_metrics = ['fit_time', 'score_time']

    # Perfomance metrics
    results_long_nofit = results_long.loc[~results_long['metrics'].isin(time_metrics)] # get df without fit data
    results_long_nofit = results_long_nofit.sort_values(by='values')

    # Time metrics
    results_long_fit = results_long.loc[results_long['metrics'].isin(time_metrics)] # df with fit data
    results_long_fit = results_long_fit.sort_values(by='values')
    metrics = list(set(results_long_nofit.metrics.values))
    model_metrics_df = bootstrap_df.groupby(['model'])[metrics].agg([np.std, np.mean])
    time_metrics = list(set(results_long_fit.metrics.values))
    time_metrics_df = bootstrap_df.groupby(['model'])[time_metrics].agg([np.std, np.mean])

    if plot:
        fig = plt.figure(figsize=(15, 10))
        spec = gridspec.GridSpec(nrows=2, ncols=1, figure=fig)
        ax1 = fig.add_subplot(spec[0])
        sns.boxplot(x="model", y="values", hue="metrics", data=results_long_nofit, palette="Set3")
        ax1.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax1.set_title('Comparison of Model by Classification Metric', pad=10)
        ax1.set_xlabel('')

        ax2 = fig.add_subplot(spec[1])
        sns.boxplot(x="model", y="values", hue="metrics", data=results_long_fit, palette="Set3")
        ax2.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        ax2.set_title('Comparison of Model by Fit and Score Time', pad=10)
        ax2.set_xlabel('')

        fig.tight_layout()
        plt.show()

    return model_metrics_df, time_metrics_df


def plot_aucroc_curve(X_train, y_train, X_test, y_test, clf):
    # Generate predictions against our training and test data
    pred_train = clf.predict(X_train)
    proba_train = clf.predict_proba(X_train)
    pred_test = clf.predict(X_test)
    proba_test = clf.predict_proba(X_test)

    # Calculate the fpr and tpr for all thresholds of the classification
    train_fpr, train_tpr, train_threshold = metrics.roc_curve(y_train, proba_train[:,1])
    test_fpr, test_tpr, test_threshold = metrics.roc_curve(y_test, proba_test[:,1])

    train_roc_auc = metrics.auc(train_fpr, train_tpr)
    test_roc_auc = metrics.auc(test_fpr, test_tpr)

    # Plot ROC-AUC curve
    plt.figure(figsize=(15, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(train_fpr, train_tpr, 'b', label='Train AUC = %0.2f' % train_roc_auc)
    plt.plot(test_fpr, test_tpr, 'g', label='Test AUC = %0.2f' % test_roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()


def plot_shap(X_test, clf):
    # Feature importance
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test, plot_type="bar", plot_size=(15, 10))
    shap.summary_plot(shap_values, X_test, plot_size=(15, 10))


def main():
    # Read data from yahoo finance API
    data = yf.download("SPY")
    dtrain = data.loc[:"2017-01-01"]
    dtest = data.loc["2017-01-01":]
    train_feature_df, X_train = generate_feature(dtrain)
    y_train = triple_barrier(dtrain, ub=1.07, lb=0.97, max_period=20, two_class=True).binary_signal
    test_feature_df, X_test = generate_feature(dtest)
    y_test = triple_barrier(dtest, ub=1.07, lb=0.97, max_period=20, two_class=True).binary_signal

    # Run model
    model_result, time_results = run_models_exps(X_train, y_train, X_test, y_test)
    print(model_result)
    print(time_result)


if __name__ == "__main__":
    main()
