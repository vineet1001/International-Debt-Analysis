# main.py

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def load_data():
    """
    Load only the columns we use, then align dtypes for merging.
    """
    # Events (not used in this minimal example, but you can extend)
    events = pd.read_parquet(
        'add_event.parquet',
        engine='pyarrow',
        columns=['id2','id3','id6','id4','id7'],
        memory_map=True
    )

    # Transactions (optional for later features)
    trans = pd.read_parquet(
        'add_trans.parquet',
        engine='pyarrow',
        columns=['id2','f367','f368','f369','f370','f371','f372','f374','id8'],
        memory_map=True
    )

    # Offers metadata
    offers = pd.read_parquet(
        'offer_metadata.parquet',
        engine='pyarrow',
        columns=['id3','f375','f376'],
        memory_map=True
    )

    # Ensure id3 is string on both sides
    offers['id3'] = offers['id3'].astype(str)

    # Train data: includes y target
    train = pd.read_parquet(
        'train_data.parquet',
        engine='pyarrow',
        columns=['id1','id2','id3','id5','y'],
        memory_map=True
    )
    # Cast to string so it matches offers.id3
    train['id3'] = train['id3'].astype(str)

    # Test data
    test = pd.read_parquet(
        'test_data.parquet',
        engine='pyarrow',
        columns=['id1','id2','id3','id5'],
        memory_map=True
    )
    test['id3'] = test['id3'].astype(str)

    # Data dictionary (optional)
    data_dict = pd.read_csv('data_dictionary.csv')

    return train, test, events, trans, offers, data_dict


def prepare_features(df, offers):
    """
    Merge in offer‐level features:
      - f375 → redeem_freq
      - f376 → discount_rate
    """
    X = df.merge(offers, on='id3', how='left')

    # Fill missing and coerce numeric
    X['f375'] = X['f375'].fillna(0).astype(float)
    X['f376'] = X['f376'].fillna(0).astype(float)

    # Rename to friendly names
    X = X.rename(columns={
        'f375': 'redeem_freq',
        'f376': 'discount_rate'
    })

    return X


def train_model(train, offers):
    """
    Builds a simple logistic regression on two features.
    """
    data = prepare_features(train, offers)
    X = data[['discount_rate','redeem_freq']]
    y = train['y'].astype(int)

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf',   LogisticRegression(max_iter=200))
    ])
    pipe.fit(X, y)
    return pipe


def make_submission(model, test, offers):
    """
    Scores test set, ranks per (id1,id2,id5), and writes top 7.
    """
    data = prepare_features(test, offers)
    X = data[['discount_rate','redeem_freq']]
    data['pred'] = model.predict_proba(X)[:,1]

    # sort descending within each user/date
    data = data.sort_values(
        ['id1','id2','id5','pred'],
        ascending=[True,True,True,False]
    )

    # pick top 7 per key
    submission = (
        data
        .groupby(['id1','id2','id5'], group_keys=False)
        .head(7)
        [['id1','id2','id3','id5','pred']]
    )

    submission.to_csv(
        'r2_submission_file_yourteam.csv',
        index=False,
        float_format='%.6f'
    )
    print("✅ Written r2_submission_file_yourteam.csv")


def main():
    train, test, events, trans, offers, data_dict = load_data()
    model = train_model(train, offers)
    make_submission(model, test, offers)


if name == 'main':
    main()