
## MUT20 Player Scraper Usage Example
- Date is only used to track scrape date, url is the first page of the pages you want to scrape on Muthead.

TODO: 
- Map archetype ids (int) to actual archetype name.


```python
from MUTScraper20 import Player, PlayerHandler, JSONParser
import pandas as pd
%load_ext autoreload
%autoreload 2

date = '23-12-2019'
url = 'https://www.muthead.com/20/players/?overall__gte=89&price_platform=2'

ph = PlayerHandler(date=date, url=url)
ph.handle_players()

jp = JSONParser(date=date)
jp.load_json()
jp.parse_json_items()
#players_to_add = ['/20/players/10128325', '/20/players/10111214', '/20/players/10110436']
#jp.add_more_players(players_to_add)
jp.jsons_to_dataframe()
jp.save_to_csv()
```

    The autoreload extension is already loaded. To reload it, use:
      %reload_ext autoreload
    Number of pages: 28
    https://www.muthead.com/20/players/?overall__gte=89&price_platform=2
    560 player links gathered.
    
    Creating file data/ST.csv


## Viewing our data


```python
import os
import pandas as pd


directory = 'data'

dfs = {}

for file in os.listdir(directory):
    if '.csv' in file:
        print(directory, file)
        dfs[file.rstrip('.csv')] = pd.read_csv(os.path.join(directory, file))
```

    data DEF.csv
    data OFF.csv
    data QB.csv
    data ST.csv



```python
dfs['QB'].sort_values('OVR', ascending=False).head(10)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>position</th>
      <th>program</th>
      <th>OVR</th>
      <th>HT</th>
      <th>WT</th>
      <th>DAC</th>
      <th>MAC</th>
      <th>SAC</th>
      <th>TAC</th>
      <th>...</th>
      <th>jersey_number</th>
      <th>last_name</th>
      <th>player_id</th>
      <th>quicksell_amount</th>
      <th>release_date</th>
      <th>salary_cap_cost</th>
      <th>team</th>
      <th>has_power_up</th>
      <th>archetype_id</th>
      <th>date_scraped</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>19</th>
      <td>Patrick Mahomes</td>
      <td>QB</td>
      <td>Ghosts of Madden - Present</td>
      <td>94</td>
      <td>75</td>
      <td>230</td>
      <td>90</td>
      <td>89</td>
      <td>91</td>
      <td>82</td>
      <td>...</td>
      <td>15</td>
      <td>Mahomes</td>
      <td>52606</td>
      <td>7430</td>
      <td>2019-12-20T15:36:43.684831Z</td>
      <td>74</td>
      <td>KC</td>
      <td>True</td>
      <td>16</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Lamar Jackson</td>
      <td>QB</td>
      <td>Blitz</td>
      <td>93</td>
      <td>74</td>
      <td>216</td>
      <td>86</td>
      <td>85</td>
      <td>89</td>
      <td>71</td>
      <td>...</td>
      <td>8</td>
      <td>Jackson</td>
      <td>51802</td>
      <td>13100</td>
      <td>2019-11-29T01:19:02.431438Z</td>
      <td>82</td>
      <td>BAL</td>
      <td>True</td>
      <td>40</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Kurt Warner</td>
      <td>QB</td>
      <td>Theme Diamonds</td>
      <td>93</td>
      <td>74</td>
      <td>214</td>
      <td>91</td>
      <td>93</td>
      <td>93</td>
      <td>93</td>
      <td>...</td>
      <td>13</td>
      <td>Warner</td>
      <td>50100</td>
      <td>13100</td>
      <td>2019-08-16T14:36:38.081332Z</td>
      <td>46</td>
      <td>LAR</td>
      <td>False</td>
      <td>4</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Lamar Jackson</td>
      <td>QB</td>
      <td>Series Redux</td>
      <td>93</td>
      <td>74</td>
      <td>216</td>
      <td>86</td>
      <td>85</td>
      <td>89</td>
      <td>71</td>
      <td>...</td>
      <td>8</td>
      <td>Jackson</td>
      <td>99951802</td>
      <td>13100</td>
      <td>2019-12-13T16:37:36.619518Z</td>
      <td>82</td>
      <td>BAL</td>
      <td>True</td>
      <td>40</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Peyton Manning</td>
      <td>QB</td>
      <td>Most Feared</td>
      <td>93</td>
      <td>77</td>
      <td>230</td>
      <td>90</td>
      <td>92</td>
      <td>93</td>
      <td>86</td>
      <td>...</td>
      <td>18</td>
      <td>Manning</td>
      <td>51623</td>
      <td>13100</td>
      <td>2019-10-25T14:36:45.598901Z</td>
      <td>46</td>
      <td>IND</td>
      <td>True</td>
      <td>4</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Ryan Fitzpatrick</td>
      <td>QB</td>
      <td>Team of the Week</td>
      <td>93</td>
      <td>74</td>
      <td>223</td>
      <td>90</td>
      <td>90</td>
      <td>93</td>
      <td>73</td>
      <td>...</td>
      <td>14</td>
      <td>Fitzpatrick</td>
      <td>56195</td>
      <td>250000</td>
      <td>2019-12-03T19:14:00.794206Z</td>
      <td>58</td>
      <td>MIA</td>
      <td>False</td>
      <td>4</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>45</th>
      <td>Randall Cunningham</td>
      <td>QB</td>
      <td>Legends</td>
      <td>93</td>
      <td>76</td>
      <td>212</td>
      <td>92</td>
      <td>83</td>
      <td>88</td>
      <td>86</td>
      <td>...</td>
      <td>12</td>
      <td>Cunningham</td>
      <td>52260</td>
      <td>13100</td>
      <td>2019-11-23T15:36:39.004217Z</td>
      <td>82</td>
      <td>PHI</td>
      <td>True</td>
      <td>40</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Derek Carr</td>
      <td>QB</td>
      <td>Signature Series</td>
      <td>92</td>
      <td>75</td>
      <td>214</td>
      <td>92</td>
      <td>89</td>
      <td>91</td>
      <td>77</td>
      <td>...</td>
      <td>4</td>
      <td>Carr</td>
      <td>51021</td>
      <td>250000</td>
      <td>2019-10-24T14:36:42.167934Z</td>
      <td>62</td>
      <td>OAK</td>
      <td>True</td>
      <td>45</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Aaron Rodgers</td>
      <td>QB</td>
      <td>Team of the Week</td>
      <td>92</td>
      <td>74</td>
      <td>225</td>
      <td>89</td>
      <td>85</td>
      <td>93</td>
      <td>84</td>
      <td>...</td>
      <td>12</td>
      <td>Rodgers</td>
      <td>56105</td>
      <td>250000</td>
      <td>2019-10-22T18:15:19.649857Z</td>
      <td>62</td>
      <td>GB</td>
      <td>True</td>
      <td>16</td>
      <td>23-12-2019</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Carson Wentz</td>
      <td>QB</td>
      <td>Series Redux</td>
      <td>92</td>
      <td>77</td>
      <td>237</td>
      <td>86</td>
      <td>89</td>
      <td>90</td>
      <td>75</td>
      <td>...</td>
      <td>11</td>
      <td>Wentz</td>
      <td>99951027</td>
      <td>9470</td>
      <td>2019-12-13T16:37:36.621550Z</td>
      <td>60</td>
      <td>PHI</td>
      <td>True</td>
      <td>16</td>
      <td>23-12-2019</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 75 columns</p>
</div>




```python

```
