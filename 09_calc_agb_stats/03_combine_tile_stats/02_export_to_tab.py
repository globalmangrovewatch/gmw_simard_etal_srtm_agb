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
out_data['Country Code'] = list()


for year in gmw_years:
    out_data[f'{year}_agb_tot'] = list()
    out_data[f'{year}_agb_avg'] = list()
    out_data[f'{year}_count'] = list()
    out_data[f'{year}_area'] = list()
    for cntry_id in country_agb_stats_lut[year]:
        if country_agb_stats_lut[year][cntry_id]['count'] > 0:
            cntry_code = country_ids_lut['val'][cntry_id]
            out_data['Country Code'].append(cntry_code)
            out_data['Country'].append(gadm_lut['gid'][cntry_code])
            out_data[f'{year}_count'].append(country_agb_stats_lut[year][cntry_id]['count'])
            out_data[f'{year}_area'].append(country_agb_stats_lut[year][cntry_id]['area'])
            out_data[f'{year}_agb_avg'].append(country_agb_stats_lut[year][cntry_id]['vals']/country_agb_stats_lut[year][cntry_id]['count'])
            out_data[f'{year}_agb_tot'].append(country_agb_stats_lut[year][cntry_id]['vals_area'])


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v314_agb_stats.csv")
df_stats.to_feather("gmw_v314_agb_stats.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v314_agb_stats.xslx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()
