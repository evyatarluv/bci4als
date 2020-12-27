# import bci4als.mi as mi
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# mi.preprocess.preprocess()
# mi.segment_data.segment_data()
# mi.extract_features.extract(mode='cnn')
# mi.assess_model.train('same day', 'svm')

# Results
# results = pd.read_csv('results.csv')
# sns.set_style(style='whitegrid')
# sns.catplot(x='Day', y='Accuracy', hue='Model', col='Subject', data=results, kind='bar')
# plt.show()

# CNN results
results = pd.read_csv('results_cnn.csv')
sns.set_style(style='whitegrid')
sns.catplot(x='Day', y='Accuracy', hue='Model', col='Subject', data=results, kind='bar', legend=False)
plt.legend(bbox_to_anchor=(1, 1))
plt.show()

