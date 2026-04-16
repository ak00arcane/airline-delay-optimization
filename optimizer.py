import pulp

def optimize(df, capacity):
    flights = df.index.tolist()
    
    model = pulp.LpProblem("Delay_Optimization", pulp.LpMinimize)
    
    delay_vars = pulp.LpVariable.dicts("delay", flights, 0, 120)
    
    # Objective
    model += pulp.lpSum([
        delay_vars[i] * df.loc[i, 'predicted_delay'] for i in flights
    ])
    
    # Capacity constraint
    for hour in df['HOUR'].unique():
        idx = df[df['HOUR'] == hour].index
        model += pulp.lpSum([delay_vars[i] for i in idx]) <= capacity
    
    model.solve()
    
    df['optimized_delay'] = [delay_vars[i].value() for i in flights]
    
    return df