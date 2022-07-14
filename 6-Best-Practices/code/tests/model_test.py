import model 

def test_prepare_features():
    model_service = ModelService(None)
    ride={
        "PULocationID":130,
        "DOLocationID":205,
        "trip_distance":3.66
    }
    actual_features = lambda_function.prepare_features(ride)
    expected_features = {
        "PU_DO":"130_205",
        "trip_distance":3.66
    }

    assert actual_features == expected_features
