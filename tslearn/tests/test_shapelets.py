import numpy as np

from tslearn.shapelets import ShapeletModel, SerializableShapeletModel

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def test_shapelets():
    n, sz, d = 15, 10, 2
    rng = np.random.RandomState(0)
    time_series = rng.randn(n, sz, d)
    y = rng.randint(2, size=n)
    clf = ShapeletModel(n_shapelets_per_size={2: 5},
                        max_iter=1,
                        verbose=0,
                        optimizer="sgd",
                        random_state=0)
    clf.fit(time_series, y)
    np.testing.assert_allclose(clf.shapelets_[0],
                               np.array([[0.56373, 0.494684],
                                         [1.235707, 1.119235]]),
                               atol=1e-2)
    np.testing.assert_allclose(clf.predict(time_series),
                               np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                                         1, 0]))

    from sklearn.model_selection import cross_validate
    cross_validate(clf, time_series, y, cv=2)


def test_serializable_shapelets():
    n, sz, d = 15, 10, 2
    rng = np.random.RandomState(0)
    time_series = rng.randn(n, sz, d)
    y = rng.randint(2, size=n)
    clf = SerializableShapeletModel(n_shapelets_per_size={2: 5},
                                    max_iter=1,
                                    verbose=0,
                                    learning_rate=0.01,
                                    random_state=0)
    clf.fit(time_series, y)
    np.testing.assert_allclose(clf.shapelets_[0],
                               np.array([[0.563342, 0.494981],
                                         [1.236804, 1.11963]]),
                               atol=1e-2)
    np.testing.assert_allclose(clf.predict(time_series),
                               np.array([0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0,
                                         1, 0]))

    params = clf.get_params(deep=True)
    for s1, s2 in zip(sorted(params.keys()),
                      sorted(['batch_size', 'learning_rate', 'max_iter',
                              'n_shapelets_per_size', 'random_state',
                              'total_lengths', 'shapelet_length', 'verbose',
                              'verbose_level', 'weight_regularizer'])):
        np.testing.assert_string_equal(s1, s2)

    from sklearn.model_selection import cross_validate
    cross_validate(clf, time_series, y, cv=2)
