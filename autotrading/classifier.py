import os
import warnings
import joblib
import datetime
import numpy as np
import pandas as pd
import xgboost as xgb
import lightgbm as lgb
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from config import Config
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn import linear_model
from sklearn import naive_bayes
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from hyperopt import tpe
from hyperopt import STATUS_OK
from hyperopt import hp
from hyperopt import Trials
from hyperopt import fmin
from optml.genetic_optimizer import GeneticOptimizer
from optml.optimizer_base import Parameter
from optml.hyperopt_optimizer import HyperoptOptimizer
warnings.filterwarnings("ignore")
global Config


def ridge_opt(X_train, y_train, X_test, y_test):
    model = linear_model.RidgeClassifier(random_state=Config.SEED)
    params = [
        Parameter(name='alpha', param_type='continuous', lower=0.01, upper=1.0)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/RIDGE_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def mlp_opt(X_train, y_train, X_test, y_test):
    model = linear_model.Perceptron(random_state=Config.SEED)
    params = [
        Parameter(name='alpha', param_type='continuous', lower=0.01, upper=1.0)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/MLP_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def sgd_opt(X_train, y_train, X_test, y_test):
    model = linear_model.SGDClassifier(random_state=Config.SEED)
    params = [
        Parameter(name='alpha', param_type='continuous', lower=0.01, upper=1.0)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/SGD_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def svm_opt(X_train, y_train, X_test, y_test):
    model = svm.SVC(random_state=Config.SEED)
    params = [
        Parameter(name='C', param_type='continuous', lower=0.01, upper=1.0)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/SVM_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def knn_opt(X_train, y_train, X_test, y_test):
    model = KNeighborsClassifier()
    params = [
        Parameter(name='n_neighbors', param_type='integer', lower=5, upper=10)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/KNN_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def gpc_opt(X_train, y_train, X_test, y_test):
    clf = GaussianProcessClassifier(kernel=1.0*RBF(1.0), random_state=Config.SEED)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/GPC_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def gnb_opt(X_train, y_train, X_test, y_test):
    clf = naive_bayes.GaussianNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/GNB_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def dtc_opt(X_train, y_train, X_test, y_test):
    model = DecisionTreeClassifier(random_state=Config.SEED)
    params = [
        Parameter(name='max_depth', param_type='integer', lower=3, upper=10),
        Parameter(name='min_samples_split', param_type='integer', lower=2, upper=5),
        Parameter(name='min_samples_leaf', param_type='continuous', lower=0, upper=0.5)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/DTC_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def ada_opt(X_train, y_train, X_test, y_test):
    model = AdaBoostClassifier(random_state=Config.SEED)
    params = [
        Parameter(name='n_estimators', param_type='integer', lower=50, upper=1000),
        Parameter(name='learning_rate', param_type='continuous', lower=0.001, upper=0.5)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/ADA_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def gbc_opt(X_train, y_train, X_test, y_test):
    model = GradientBoostingClassifier(random_state=Config.SEED)
    params = [
        Parameter(name='n_estimators', param_type='integer', lower=50, upper=1000),
        Parameter(name='max_depth', param_type='integer', lower=3, upper=10),
        Parameter(name='learning_rate', param_type='continuous', lower=0.001, upper=0.5),
        Parameter(name='min_samples_split', param_type='continuous', lower=0, upper=0.5),
        Parameter(name='min_samples_leaf', param_type='continuous', lower=0, upper=0.5)]
    optimizer = HyperoptOptimizer(
        model=model,
        eval_func=roc_auc_score,
        hyperparams=params)
    _, clf = optimizer.fit(X_train, y_train, n_iters=Config.HYPEROPT_MAX_EVAL)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/GBC_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def lgbm_opt(X_train, y_train, X_test, y_test):
    kf = KFold(n_splits=Config.KFOLD, random_state=Config.SEED)

    def roc_auc_cv(params, random_state=Config.SEED, cv=kf, X=X_train, y=y_train):
        params = {
            'n_estimators': int(params['n_estimators']),
            'max_depth': int(params['max_depth']),
            'learning_rate': params['learning_rate']}
        model = lgb.LGBMClassifier(random_state=random_state, num_leaves=4, **params)
        score = -cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1).mean()
        return score

    space = {
        'n_estimators': hp.quniform('n_estimators', 100, 2000, 1),
        'max_depth' : hp.quniform('max_depth', 4, 20, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0)}
    trials = Trials()
    best = fmin(
        fn=roc_auc_cv, space=space, algo=tpe.suggest,
        max_evals=Config.HYPEROPT_MAX_EVAL, trials=trials, rstate=np.random.RandomState(Config.SEED))
    clf = lgb.LGBMClassifier(
        random_state=Config.SEED, n_estimators=int(best['n_estimators']),
        max_depth=int(best['max_depth']),learning_rate=best['learning_rate'])
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/LGBM_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def xgb_opt(X_train, y_train, X_test, y_test):
    kf = KFold(n_splits=Config.KFOLD, random_state=Config.SEED)

    def roc_auc_cv(params, random_state=Config.SEED, cv=kf, X=X_train, y=y_train):
        params = {
            'n_estimators': int(params['n_estimators']),
            'max_depth': int(params['max_depth']),
            'learning_rate': params['learning_rate'],
            'min_child_weight': params['min_child_weight'],
            'colsample_bytree': params['colsample_bytree'],
            'gamma': params['gamma'],
            'subsample': params['subsample']}
        model = xgb.XGBClassifier(random_state=random_state, **params)
        score = -cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1).mean()
        return score

    space = {
        'n_estimators': hp.quniform('n_estimators', 100, 2000, 1),
        'max_depth' : hp.quniform('max_depth', 4, 20, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'min_child_weight': hp.quniform('min_child_weight', 1, 6, 1),
        'colsample_bytree': hp.quniform('colsample_bytree', 0.6, 1, 0.05),
        'subsample': hp.quniform('subsample', 0.6, 1, 0.05),
        'gamma': hp.quniform('gamma', 0.5, 10, 0.05)}
    trials = Trials()
    best = fmin(
        fn=roc_auc_cv, space=space, algo=tpe.suggest,
        max_evals=Config.HYPEROPT_MAX_EVAL, trials=trials, rstate=np.random.RandomState(Config.SEED))
    clf = xgb.XGBClassifier(
        random_state=Config.SEED, n_estimators=int(best['n_estimators']),
        max_depth=int(best['max_depth']),learning_rate=best['learning_rate'],
        min_child_weight=best['min_child_weight'], colsample_bytree=best['colsample_bytree'],
        gamma=best['gamma'], subsample=best['subsample'])
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/XGB_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred


def cat_opt(X_train, y_train, X_test, y_test):
    kf = KFold(n_splits=Config.KFOLD, random_state=Config.SEED)

    def roc_auc_cv(params, random_state=Config.SEED, cv=kf, X=X_train, y=y_train):
        params = {
            'depth': int(params['depth']),
            'learning_rate': params['learning_rate']}
        model = CatBoostClassifier(iterations=10, random_seed=random_state, silent=True, **params)
        score = -cross_val_score(model, X, y, cv=cv, scoring="roc_auc", n_jobs=-1).mean()
        return score

    space = {
        'depth': hp.quniform('depth', 4, 10, 1),
        'learning_rate': hp.loguniform('learning_rate', -4, 0)}
    trials = Trials()
    best = fmin(
        fn=roc_auc_cv, space=space, algo=tpe.suggest,
        max_evals=Config.HYPEROPT_MAX_EVAL, trials=trials, rstate=np.random.RandomState(Config.SEED))
    clf = CatBoostClassifier(
        iterations=10, random_state=Config.SEED, silent=True,
        depth=int(best['depth']),learning_rate=best['learning_rate'])
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    if Config.PRINT_CLASSIFICATION_REPORT:
        print(classification_report(y_test, y_pred))

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/CAT_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    return clf, y_pred
