import matplotlib as mpl

# Apparently, SNS stands for "Samuel Norman Seaborn", a fictional
# character from The West Wing
import seaborn as sns

sns.set()
# Increase default figure size and DPI
mpl.rcParams["figure.figsize"] = (7.68, 5.76)
mpl.rcParams["figure.dpi"] = 300
mpl.rcParams["savefig.bbox"] = "tight"
