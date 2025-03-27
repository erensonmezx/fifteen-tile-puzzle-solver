# src/image_processing/image_handler.py
from typing import List, Optional, Tuple

import cv2
import numpy as np


class ImageHandler:
    def __init__(self):
        self.original_image = None
        self.tiles = []
        self.tile_size = (0, 0)

    def load_image(self, path: str, target_size: Tuple[int, int] = (300, 300)) -> bool:
        """Load and resize image."""
        try:
            self.original_image = cv2.imread(path)
            if self.original_image is None:
                raise ValueError(f"Failed to load image from {path}")
                
            # Resize to target size
            self.original_image = cv2.resize(self.original_image, target_size)
            
            # Calculate tile size
            height, width = self.original_image.shape[:2]
            self.tile_size = (width // 4, height // 4)
            
            return True
        except Exception as e:
            print(f"Error loading image: {e}")
            self.original_image = None
            self.tiles = []
            self.tile_size = (0, 0)
            return False

    def split_image(self) -> List[np.ndarray]:
        """Split image into 4x4 grid."""
        if self.original_image is None:
            raise ValueError("Image not loaded. Please load an image first.")
        
        height, width = self.original_image.shape[:2]
        if height % 4 != 0 or width % 4 != 0:
            raise ValueError("Image dimensions must be divisible by 4")

        self.tiles = []
        tile_height, tile_width = self.tile_size[1], self.tile_size[0]

        for i in range(4):
            for j in range(4):
                y_start = i * tile_height
                y_end = (i + 1) * tile_height
                x_start = j * tile_width
                x_end = (j + 1) * tile_width
                
                tile = self.original_image[y_start:y_end, x_start:x_end].copy()
                self.tiles.append(tile)

        return self.tiles

    def merge_tiles(self, tile_order: List[int]) -> np.ndarray:
        """Merge tiles based on given order."""
        if not self.tiles:
            raise ValueError("No tiles available. Split an image first.")
        if len(tile_order) != 16:  # Change from 9 to 16
            raise ValueError("Invalid tile order. Must have exactly 16 positions.")
        
        # Create blank merged image
        height = self.tile_size[1] * 4  # Change from 3 to 4
        width = self.tile_size[0] * 4  # Change from 3 to 4
        merged = np.zeros((height, width, 3), dtype=np.uint8)  # Ensure 3 channels for RGB
        
        for i in range(4):  # Change from 3 to 4
            for j in range(4):  # Change from 3 to 4
                idx = i * 4 + j  # Change from 3 to 4
                tile_idx = tile_order[idx]
                
                y_start = i * self.tile_size[1]
                y_end = (i + 1) * self.tile_size[1]
                x_start = j * self.tile_size[0]
                x_end = (j + 1) * self.tile_size[0]
                
                if tile_idx == 0:  # Blank tile
                    merged[y_start:y_end, x_start:x_end] = 255  # White
                else:
                    merged[y_start:y_end, x_start:x_end] = self.tiles[tile_idx - 1]
                    
        return merged

    # def get_tile(self, index: int) -> Optional[np.ndarray]:
    #     """Get tile by index safely."""
    #     if not self.tiles:
    #         raise ValueError("No tiles available")
    #     if not 0 <= index < len(self.tiles):
    #         raise ValueError(f"Invalid tile index: {index}")
    #     return self.tiles[index]