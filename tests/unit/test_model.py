"""
Unit tests for MovieRatingModel class.

TODO: Complete the test implementations below.

Run tests:
    pytest tests/unit/test_model.py -v
"""

import pytest
from app.model import MovieRatingModel


class TestMovieRatingModel:
    """Unit tests for MovieRatingModel class."""
    
    # =========================================================================
    # Model Loading Tests
    # =========================================================================
    
    def test_model_loads_successfully(self, trained_model):
        """Test that model loads without errors."""
        assert trained_model is not None
        assert trained_model.is_loaded()
    
    def test_model_instance_has_model_attribute(self, trained_model):
        """Test that model instance has the model attribute."""
        assert hasattr(trained_model, "model")
        assert trained_model.model is not None
    
    # =========================================================================
    # TODO 1: Implement Prediction Return Type Tests
    # =========================================================================
    
    def test_predict_returns_float(self, trained_model):
        """Test that predict() returns a float value."""
        result = trained_model.predict("196", "242")
        assert isinstance(result, float)
    
    # =========================================================================
    # TODO 2: Implement Rating Range Tests
    # =========================================================================
    
    def test_predict_returns_value_in_valid_range(self, trained_model):
        """Test that predictions are within 1-5 range."""
        result = trained_model.predict("196", "242")
        assert 1.0 <= result <= 5.0
    
    def test_predict_multiple_pairs_all_in_range(self, trained_model, known_user_movie_pairs):
        """Test that all predictions are in valid range."""
        for pair in known_user_movie_pairs:
            result = trained_model.predict(pair["user_id"], pair["movie_id"])
            assert 1.0 <= result <= 5.0
    
    # =========================================================================
    # TODO 3: Implement Batch Prediction Tests
    # =========================================================================
    
    def test_predict_batch_returns_list(self, trained_model):
        """Test that predict_batch() returns a list."""
        pairs = [("196", "242"), ("186", "302")]
        results = trained_model.predict_batch(pairs)
        assert isinstance(results, list)
    
    def test_predict_batch_returns_correct_length(self, trained_model):
        """Test that predict_batch() returns correct number of results."""
        pairs = [("196", "242"), ("186", "302"), ("22", "377")]
        results = trained_model.predict_batch(pairs)
        assert len(results) == len(pairs)
    
    def test_predict_batch_all_values_in_range(self, trained_model):
        """Test that all batch predictions are in valid range."""
        pairs = [("196", "242"), ("186", "302"), ("22", "377")]
        results = trained_model.predict_batch(pairs)
        for rating in results:
            assert isinstance(rating, float)
            assert 1.0 <= rating <= 5.0
    
    # =========================================================================
    # TODO 4: Implement is_loaded() Tests
    # =========================================================================
    
    def test_is_loaded_returns_bool(self, trained_model):
        """Test that is_loaded() returns a boolean."""
        result = trained_model.is_loaded()
        assert isinstance(result, bool)
    
    def test_is_loaded_returns_true_for_loaded_model(self, trained_model):
        """Test that is_loaded() returns True for loaded model."""
        assert trained_model.is_loaded() is True
    
    # =========================================================================
    # TODO 5: Implement Error Handling Tests (BONUS)
    # =========================================================================
    
    def test_predict_with_none_user_id(self, trained_model):
        """Test behavior when user_id is None."""
        try:
            result = trained_model.predict(None, "242")
            assert isinstance(result, float)
            assert 1.0 <= result <= 5.0
        except Exception as e:
            assert isinstance(e, (TypeError, AttributeError, ValueError))
    
    def test_predict_with_empty_string(self, trained_model):
        """Test behavior when IDs are empty strings."""
        result = trained_model.predict("", "")
        assert isinstance(result, float)
        assert 1.0 <= result <= 5.0


class TestModelFileHandling:
    """Tests for model file handling."""
    
    def test_model_raises_error_for_missing_file(self):
        """Test that missing model file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            MovieRatingModel(model_path="/nonexistent/path/model.pkl")

    def test_model_raises_error_for_corrupted_file(self, tmp_path):
        """Test that corrupted model file raises exception."""
        bad_file = tmp_path / "corrupt.pkl"
        bad_file.write_bytes(b"invalid pickle data")
        with pytest.raises(Exception):
            MovieRatingModel(model_path=str(bad_file))

    def test_unloaded_model_raises_runtime_error(self, trained_model):
        """Test that predict() and predict_batch() raise RuntimeError when model is None."""
        original_inner_model = trained_model.model
        try:
            trained_model.model = None
            with pytest.raises(RuntimeError):
                trained_model.predict("196", "242")
            with pytest.raises(RuntimeError):
                trained_model.predict_batch([("196", "242")])
        finally:
            trained_model.model = original_inner_model

    def test_get_model_and_reset_model(self):
        """Test get_model singleton and reset_model helper functions."""
        from app.model import get_model, reset_model
        reset_model()
        m1 = get_model()
        m2 = get_model()
        assert m1 is m2
        reset_model()

    def test_baseline_rating_model_fit(self):
        """Test BaselineRatingModel fit method."""
        from app.simple_model import BaselineRatingModel
        bm = BaselineRatingModel()
        assert bm.fit() is bm


# =============================================================================
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
