# Spotify 2023 Data Preprocessing and Analysis

This repository contains data mining preparation and exploratory data analysis (EDA) for the "Most Streamed Spotify Songs 2023" dataset.

## Dataset Overview

The dataset contains information about the most streamed songs on Spotify in 2023, including:
- **Track information**: Song names, artist names, release dates
- **Streaming metrics**: Streams across different platforms (Spotify, Apple Music, Deezer, Shazam)
- **Musical attributes**: BPM, key, mode, danceability, valence, energy, acousticness, etc.
- **Platform presence**: Chart positions and playlist inclusions

## Project Structure

```
├── spotify-2023.csv          # Original dataset (954 songs)
├── EDA.ipynb                 # Exploratory Data Analysis notebook
├── DMA.ipynb                 # Data Mining preparation notebook
├── df_norm.csv               # Normalized dataset output (50 samples)
├── df_disc_num.csv           # Discretized dataset output (50 samples)
└── README.md                 # This documentation
```

## Notebooks Description

### 1. EDA.ipynb - Exploratory Data Analysis

This notebook performs exploratory analysis of the Spotify dataset:

#### Data Quality Assessment
- **Duplicate detection**: Identifies and handles duplicate records
- **Missing value analysis**: Evaluation of null values across all columns
- **Data type validation**: Ensures proper data types for analysis

#### Data Cleaning
- **Streams column**: Converts string values to numeric, removes invalid entries
- **Shazam charts**: Handles comma-separated values and converts to numeric
- **Deezer playlists**: Processes formatting issues and converts to numeric

#### Statistical Analysis
- **Descriptive statistics**: Mean, median, standard deviation for all numerical attributes
- **Frequency analysis**: Distribution of categorical variables (key, mode, artists)
- **Correlation analysis**: Heatmap visualization of relationships between numerical features


#### Visualizations
- **Distribution plots**: Histograms and violin plots for key variables
- **3D scatter plots**: Multi-dimensional analysis of BPM, streams, and energy
- **Box plots**: Distribution analysis by categorical variables (key, mode)
- **Correlation heatmaps**: Visual representation of feature relationships

#### Statistical Testing
- **T-tests**: Pairwise comparisons between different musical keys
- **Outlier detection**: Multiple methods including:
  - IQR (Interquartile Range) method
  - Z-score analysis

### 2. DMA.ipynb - Data Mining Preparation

This notebook prepares the data for data mining tasks with focus on platform comparison analysis:

#### Data Preprocessing
- **Column removal**: Eliminates unnecessary date columns (released_month, released_day)
- **Missing value handling**:
  - Removes rows with missing 'key' values (essential for music analysis)
  - Fills missing Shazam chart positions with max_rank + 1
  - Fills missing Deezer playlist values with 0

#### Data Type Conversion
- **Numeric conversion**: Ensures proper data types for streams and playlist counts
- **Error handling**: Uses 'coerce' to handle conversion errors gracefully

#### Outlier Treatment
- **IQR-based capping**: Replaces extreme outliers in streams with calculated upper bounds
- **Visual validation**: Box plots to verify outlier treatment effectiveness

#### Dataset Preparation for Mining

**Normalized Dataset (df_norm.csv)**:
- **Min-Max scaling**: Normalizes all numerical features to [0,1] range
- **One-hot encoding**: Converts categorical variables (key, mode) to binary features
- **Feature selection**: Excludes non-essential columns (artist_count, released_year from normalization)

**Discretized Dataset (df_disc_num.csv)**:
- **Quantile-based discretization**: Converts numerical features to categorical labels
- **Custom binning**: Uses meaningful labels (very low, low, high, very high)
- **Special handling**: Addresses features with limited unique values



## Technical Implementation

### Libraries Used
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib/seaborn**: Statistical visualizations
- **plotly**: Interactive 3D visualizations
- **scikit-learn**: Machine learning preprocessing and outlier detection
- **scipy**: Statistical testing

## Results

### Key Findings from EDA
- Most songs are from recent years (post-2010)
- Strong correlations between certain audio features
- Platform-specific popularity patterns
- Musical key preferences in popular music

### Dataset Characteristics
- **Original size**: 954 songs with 24 attributes
- **Post-cleaning**: Minimal data loss with improved quality
- **Feature distribution**: Well-balanced across most categorical variables
- **Outlier impact**: Manageable outlier presence across numerical features
