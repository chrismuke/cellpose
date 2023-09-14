from pathlib import Path
import numpy as np
import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('path', type=str, help='an integer for the accumulator')
    args = parser.parse_args()
    print(args.path)

    # p = Path('D:\\mina\\Test Quantifizierung')
    p = Path(args.path)

    area_pixel = 0.512 * 0.512
    cells = p / "cells"
    exclude = p / "exclude"
    results = []
    for c in cells.glob("**/*.npy"):
        print(c)
        e = exclude / c.name
        if not e.exists():
            print(f"{e} does not exist. Skipping ...")
            continue
        dc = np.load(c, allow_pickle=True).item()
        num_cells = dc["masks"].max()
        de = np.load(e, allow_pickle=True).item()
        masks = de["masks"]
        num_pixels = masks.shape[0] * masks.shape[1] - np.count_nonzero(masks)
        area = num_pixels * area_pixel
        print(area)
        cells_per_um2 = num_cells / area
        print(cells_per_um2)
        parts = c.parts
        group = parts[-3]
        mouse = parts[-2]
        row = {'group': group, 'mouse': mouse, 'filename': c, 'num_cells': num_cells, 'area': area, 'cells_per_um2': cells_per_um2}
        print(row)
        results.append(row)
    df = pd.DataFrame(results)
    df.to_excel(p / 'results.xlsx')
