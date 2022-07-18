import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../03_define_country_extents/01_define_country_ids/gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_agb_stats_file = '/home/pete/Documents/gmw_v3_agb_hgt/stats/country_agb_hists.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)


out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['0-250'] = list()
out_data['250-500'] = list()
out_data['500-750'] = list()
out_data['750-1000'] = list()
out_data['1000-1250'] = list()
out_data['1250-'] = list()


for cntry_id in country_ids_lut["val"].keys():
    country_agb_arr = numpy.array(country_agb_stats_lut[cntry_id], dtype=numpy.uint32)
    if numpy.sum(country_agb_arr) > 0:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['0-250'].append(numpy.sum(country_agb_arr[0:10]))
        out_data['250-500'].append(numpy.sum(country_agb_arr[10:20]))
        out_data['500-750'].append(numpy.sum(country_agb_arr[20:30]))
        out_data['750-1000'].append(numpy.sum(country_agb_arr[30:40]))
        out_data['1000-1250'].append(numpy.sum(country_agb_arr[40:50]))
        out_data['1250-'].append(numpy.sum(country_agb_arr[50:]))


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_agb_summary_bounds.csv")
df_stats.to_feather("gmw_v3_agb_summary_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_agb_summary_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()
