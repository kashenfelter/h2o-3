import sys
sys.path.insert(1,"../../../")
import h2o, tests
from h2o.estimators.deeplearning import H2ODeepLearningEstimator

def checkpoint_new_category_in_predictor():

  sv1 = h2o.upload_file(tests.locate("smalldata/iris/setosa_versicolor.csv"))
  sv2 = h2o.upload_file(tests.locate("smalldata/iris/setosa_versicolor.csv"))
  vir = h2o.upload_file(tests.locate("smalldata/iris/virginica.csv"))

  m1 = H2ODeepLearningEstimator(epochs=100)
  m1.train(X=[0,1,2,4], y=3, training_frame=sv1)

  m2 = H2ODeepLearningEstimator(epochs=200, checkpoint=m1.model_id)
  m2.train(X=[0,1,2,4], y=3, training_frame=sv2)

  # attempt to continue building model, but with an expanded categorical predictor domain.
  # this should fail
  try:
    m3 = H2ODeepLearningEstimator(epochs=200, checkpoint=m1.model_id)
    m3.train(X=[0,1,2,4], y=3, training_frame=vir)
    assert False, "Expected continued model-building to fail with new categories introduced in predictor"
  except EnvironmentError:
    pass

  # attempt to predict on new model, but with observations that have expanded categorical predictor domain.
  predictions = m2.predict(vir)

if __name__ == '__main__':
  tests.run_test(sys.argv, checkpoint_new_category_in_predictor)
