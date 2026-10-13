"""Post-process pipeline: outline, quantize, alpha trim."""
import numpy as np
from PIL import Image

from spriteforge.config.schema import PostProcessConfig
from spriteforge.core.post