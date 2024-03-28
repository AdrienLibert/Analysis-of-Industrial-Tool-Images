import pandas as pd


df = pd.read_csv('TableauConversion/Metrique.csv')
df.columns = ['Type', 'Diamètre', 'Pas']

def pattern_list(df):
    df.columns = ['Type', 'Diamètre', 'Pas']
    l = []
    for index, row in df.iterrows():
        metric_str = row['Diamètre']
        if pd.notna(metric_str) and "M" in metric_str:
            try:
                diam_mm = float(metric_str.replace("M", "").replace(",", "."))
            except ValueError:
                continue
            pas_value = row['Pas']
            if pd.notna(pas_value):
                l.append((diam_mm, pas_value/100))
    return l
