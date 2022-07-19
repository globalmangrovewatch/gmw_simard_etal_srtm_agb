import rsgislib.tools.utils
import pandas
import numpy

country_agb_stats_file = 'country_agb_hists.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)

glb_out_data = numpy.zeros((81), dtype=numpy.uint32)

for cntry_id in country_agb_stats_lut:
    country_agb_arr = numpy.array(country_agb_stats_lut[cntry_id], dtype=numpy.uint32)
    glb_out_data = glb_out_data + country_agb_arr

agb_bins = numpy.arange(0, 2025, 25)
glb_out_data_dict = dict()
for i in range(81):
    glb_out_data_dict[f"{agb_bins[i]}"] = [glb_out_data[i]]

df_stats = pandas.DataFrame.from_dict(glb_out_data_dict)
df_stats.to_csv("gmw_v3_agb_glb_hist.csv")
df_stats.to_feather("gmw_v3_agb_glb_hist.feather")
xlsx_writer = pandas.ExcelWriter("gmw_v3_agb_glb_hist.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='gmw_agb_stats')
xlsx_writer.save()
