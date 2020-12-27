# import bci4als.mi as mi
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# mi.preprocess.preprocess()
# mi.segment_data.segment_data()
# mi.extract_features.extract()
# mi.assess_model.train('same day', 'rf')

results = pd.read_csv('../data/results.csv')
sns.set_theme(style='whitegrid')
sns.catplot(x='day', y='accuracy', hue='model', col='subject', data=results, kind='bar')
plt.show()


