import h5py
with h5py.File('model.h5', 'r') as f:
    print("File opened successfully.")
