import pytest
from unittest.mock import patch
from ai_optix.core.selector import SmartSelector

class TestSmartSelector:
    @pytest.fixture
    def mock_device_manager(self):
        with patch("ai_optix.core.selector.DeviceManager") as MockDM:
            instance = MockDM.return_value
            # Default to having a generic CUDA device
            instance.info = {
                "device_type": "cuda",
                "device_name": "NVIDIA FakeGPU",
                "device_count": 1
            }
            yield instance

    def test_init_detects_gpu(self, mock_device_manager):
        """Test that selector correctly identifies GPU availability from manager."""
        selector = SmartSelector(use_gpu_if_available=True)
        assert selector.has_gpu is True
        assert selector.device_info["device_type"] == "cuda"

    def test_init_obeys_flag(self, mock_device_manager):
        """Test that use_gpu_if_available=False forces CPU."""
        selector = SmartSelector(use_gpu_if_available=False)
        assert selector.has_gpu is False

    def test_select_cpu_for_small_linear(self, mock_device_manager):
        """Small linear ops should prefer CPU to avoid transfer overhead."""
        selector = SmartSelector()
        # Shape (100,) linear op is tiny. Transfer cost > Compute gain.
        choice = selector.select_device((100,), op_complexity_str="linear")
        assert choice == "cpu"

    def test_select_gpu_for_large_cubic(self, mock_device_manager):
        """Large cubic ops (MatMul) should prefer GPU."""
        selector = SmartSelector()
        # Shape (2048, 2048) MatMul is computationally heavy.
        # 2048*2048 elements. Cubic complexity.
        choice = selector.select_device((2048, 2048), op_complexity_str="cubic")
        assert choice == "cuda"

    def test_fallback_when_no_gpu(self):
        """If no GPU matches, it must return CPU."""
        with patch("ai_optix.core.selector.DeviceManager") as MockDM:
            instance = MockDM.return_value
            instance.info = {"device_type": "cpu"}
            
            selector = SmartSelector()
            assert selector.has_gpu is False
            choice = selector.select_device((4096, 4096), "cubic")
            assert choice == "cpu"
