import sys

sys.path.append("./")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import ensemble
from sklearn.model_selection import train_test_split

from api.chalicelib.db import connection

with connection() as conn:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT cast(date_trunc('week', date) as date) as week, * FROM record
            LEFT JOIN ad_unit ON record.admob_ad_unit_id = ad_unit.admob_ad_unit_id
            LEFT JOIN app ON ad_unit.admob_app_id = app.admob_app_id
            LEFT JOIN app_external ON app.id = app_external.app_id
            LEFT JOIN publisher ON app.admob_publisher_id = publisher.admob_publisher_id
            LEFT JOIN account ON publisher.account_id = account.id
            WHERE impressions > 20
        """
        )
        rows = cur.fetchall()
df = pd.DataFrame(rows)
df["month"] = df["week"].map(lambda x: x.month)

print(df.columns, df.shape)


y = (df["earnings"] / 1000.0) / df["impressions"]

X = df[["month", "country", "serving_restriction", "format", "platform", "genre"]]
X = pd.get_dummies(data=X, drop_first=True)


X_train, X_test, Y_train, Y_test = train_test_split(
    X, y, test_size=0.20, random_state=40
)

regr = ensemble.RandomForestRegressor()
regr.fit(X_train, Y_train)
predicted = regr.predict(X_test)

print(regr.score(X_test, Y_test))


fig = plt.figure()
plt.scatter(regr.predict(X_test), Y_test, figure=fig)
plt.plot(range(0, 20), range(0, 20), figure=fig)
plt.show()
