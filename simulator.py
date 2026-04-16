import numpy as np

def simulate(df):
    simulated = []
    
    for _, row in df.iterrows():
        noise = np.random.normal(0, 5)
        delay = max(0, row['optimized_delay'] + noise)
        simulated.append(delay)
    
    df['simulated_delay'] = simulated
    
    return df