import rsgislib.tools.utils
import pandas

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../03_define_country_extents/01_define_country_ids/gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_hchm_stats_file = '/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/country_hchm_stats.json'
country_hchm_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_hchm_stats_file)

gmw_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']

out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()

for year in gmw_years:
    out_data[f'{year}_hchm_avg'] = list()
    out_data[f'{year}_count'] = list()

for cntry_id in country_ids_lut["val"].keys():
    have_data = False
    for year in gmw_years:
        if country_hchm_stats_lut[year][cntry_id]['count'] > 0:
            have_data = True
            break

    if have_data:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])

        for year in gmw_years:
            out_data[f'{year}_count'].append(country_hchm_stats_lut[year][cntry_id]['count'])
            out_data[f'{year}_hchm_avg'].append(country_hchm_stats_lut[year][cntry_id]['vals']/country_hchm_stats_lut[year][cntry_id]['count'])



print('Country: {}'.format(len(out_data['Country'])))
print('Country_Code: {}'.format(len(out_data['Country_Code'])))

for year in gmw_years:
    print('{}_hchm_avg: {}'.format(year, len(out_data[f'{year}_hchm_avg'])))
    print('{}_count: {}'.format(year, len(out_data[f'{year}_count'])))
    print("")


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v314_hchm_stats.csv")
df_stats.to_feather("gmw_v314_hchm_stats.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v314_hchm_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_hchm_stats')
xlsx_writer.save()
