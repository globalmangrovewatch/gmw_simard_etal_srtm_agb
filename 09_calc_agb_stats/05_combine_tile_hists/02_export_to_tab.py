import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../03_define_country_extents/01_define_country_ids/gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_agb_stats_file = 'country_agb_hists.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)


out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['0-50'] = list()
out_data['50-100'] = list()
out_data['100-150'] = list()
out_data['150-250'] = list()
out_data['250-1500'] = list()


for cntry_id in country_ids_lut["val"].keys():
    country_agb_arr = numpy.array(country_agb_stats_lut[cntry_id], dtype=numpy.uint32)
    tot_country_agb = numpy.sum(country_agb_arr)
    if tot_country_agb > 0:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['0-50'].append(numpy.sum(country_agb_arr[0:2])/tot_country_agb)
        out_data['50-100'].append(numpy.sum(country_agb_arr[2:4])/tot_country_agb)
        out_data['100-150'].append(numpy.sum(country_agb_arr[4:6])/tot_country_agb)
        out_data['150-250'].append(numpy.sum(country_agb_arr[6:10])/tot_country_agb)
        out_data['250-1500'].append(numpy.sum(country_agb_arr[10:])/tot_country_agb)


df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("gmw_v3_agb_summary_bounds.csv")
df_stats.to_feather("gmw_v3_agb_summary_bounds.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_agb_summary_bounds.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()
