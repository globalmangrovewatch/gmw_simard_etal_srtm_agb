import rsgislib.tools.utils
import pandas

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../03_define_country_extents/01_define_country_ids/gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_agb_stats_file = '/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/country_agb_stats.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)

gmw_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']

out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()

for year in gmw_years:
    out_data[f'{year}_agb_tot'] = list()
    out_data[f'{year}_agb_avg'] = list()
    out_data[f'{year}_count'] = list()
    out_data[f'{year}_area'] = list()

for cntry_id in country_ids_lut["val"].keys():
    have_data = False
    for year in gmw_years:
        if country_agb_stats_lut[year][cntry_id]['count'] > 0:
            have_data = True
            break

    if have_data:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])

        for year in gmw_years:
            out_data[f'{year}_count'].append(country_agb_stats_lut[year][cntry_id]['count'])
            out_data[f'{year}_area'].append(country_agb_stats_lut[year][cntry_id]['area'])
            out_data[f'{year}_agb_avg'].append(country_agb_stats_lut[year][cntry_id]['vals']/country_agb_stats_lut[year][cntry_id]['count'])
            out_data[f'{year}_agb_tot'].append(country_agb_stats_lut[year][cntry_id]['vals_area'])



print('Country: {}'.format(len(out_data['Country'])))
print('Country_Code: {}'.format(len(out_data['Country_Code'])))

for year in gmw_years:
    print('{}_agb_tot: {}'.format(year, len(out_data[f'{year}_agb_tot'])))
    print('{}_agb_avg: {}'.format(year, len(out_data[f'{year}_agb_avg'])))
    print('{}_count: {}'.format(year, len(out_data[f'{year}_count'])))
    print('{}_area: {}'.format(year, len(out_data[f'{year}_area'])))
    print("")


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v314_agb_stats.csv")
df_stats.to_feather("gmw_v314_agb_stats.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v314_agb_stats.xslx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()
