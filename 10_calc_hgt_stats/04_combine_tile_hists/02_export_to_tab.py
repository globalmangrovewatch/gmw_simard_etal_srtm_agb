import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../03_define_country_extents/01_define_country_ids/gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_hchm_stats_file = '/home/pete/Documents/gmw_v3_agb_hgt/stats/country_hchm_hists.json'
country_hchm_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_hchm_stats_file)


out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['0-13'] = list()
out_data['13-26'] = list()
out_data['26-39'] = list()
out_data['39-52'] = list()
out_data['52-65'] = list()
out_data['65-'] = list()


for cntry_id in country_ids_lut["val"].keys():
    country_hchm_arr = numpy.array(country_hchm_stats_lut[cntry_id], dtype=numpy.uint32)
    tot_country_hchm = numpy.sum(country_hchm_arr)
    if tot_country_hchm > 0:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['0-13'].append(numpy.sum(country_hchm_arr[0:13])/tot_country_hchm)
        out_data['13-26'].append(numpy.sum(country_hchm_arr[13:26])/tot_country_hchm)
        out_data['26-39'].append(numpy.sum(country_hchm_arr[26:39])/tot_country_hchm)
        out_data['39-52'].append(numpy.sum(country_hchm_arr[39:52])/tot_country_hchm)
        out_data['52-65'].append(numpy.sum(country_hchm_arr[52:65])/tot_country_hchm)
        out_data['65-'].append(numpy.sum(country_hchm_arr[65:])/tot_country_hchm)


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_hchm_summary_bounds.csv")
df_stats.to_feather("gmw_v3_hchm_summary_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_hchm_summary_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_hchm_stats')
xlsx_writer.save()
