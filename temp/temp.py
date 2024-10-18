# elif len(data)-1 > 1:
#             # pega os dados em variáveis
#             hexadecimal,fornecedores = (data[card]['hexadecimal']), data[card]['fornecedores']
#             nome,pantone_codigo = data[card]['nome'],data[card] ['pantone_código']
#             red,green,blue = data[card]['red'],data[card]['green'],data[card]['blue']
#             c,y,m,k = rgb_to_cmyk(data[card]['red'],data[card]['green'],data[card]['blue'])
#             hexadecimal1,fornecedores1 = (data[card+1]['hexadecimal']), data[card+1]['fornecedores']
#             nome1,pantone_codigo1 = data[card+1]['nome'],data[card+1] ['pantone_código']
#             red1,green1,blue1 = data[card+1]['red'],data[card+1]['green'],data[card+1]['blue']
#             c1,y1,m1,k1 = rgb_to_cmyk(data[card+1]['red'],data[card+1]['green'],data[card+1]['blue'])
#             hexadecimal2,fornecedores2 = (data[card+2]['hexadecimal']), data[card+2]['fornecedores']
#             nome2,pantone_codigo2 = data[card+2]['nome'],data[card+2]['pantone_código']
#             red2,green2,blue2 = data[card+2]['red'],data[card+2]['green'],data[card+2]['blue']
#             c2,y2,m2,k2 = rgb_to_cmyk(data[card+2]['red'],data[card+2]['green'],data[card+2]['blue'])
        
#             with container:
#                 st.button('anterior', key='anterior', on_click=subtract_count)
#                 script = ("<div style='display: flex; flex-direction: row; justify-content: space-around; margin: 0px; padding:0px;width: 700px ;margin: 0px auto; height: 450px;'><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'><div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p><p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f} <br>magenta: {:.2f} <br>key:{:.2f} </p> </div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'> <div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f} <br>magenta: {:.2f} <br>key:{:.2f} </p> </div><div style='background-color: white ; width: 220px; height: 400px;border-radius: 10px; padding: 10px;box-shadow: 2px 2px 2px 1.5px rgba(0, 0, 0, 0.25); margin: 5px;'> <div id='container' style='background-color: {}; width: 200px; height: 200px; '></div> <p style='color:black; margin: 0px; padding:0px'>{}: {}</p> <p style='color:black;margin: 0px; padding:0px;'>pantone: {}</p> <p style='color:black;margin: 0px; padding:0px'>rgb: {},{},{} </p> <p style='color:black;margin: 0px; padding:0px'>cyan: {:.2f} <br>yellow: {:.2f}<br>magenta: {:.2f}<br>key:{:.2f} </p> </div></div>").format(hexadecimal,fornecedores,nome,pantone_codigo,red,green,blue,float(c),float(m),float(y),float(k),hexadecimal1,fornecedores1,nome1,pantone_codigo1,red1,green1,blue1,float(c1),float(m1),float(y1),float(k1),hexadecimal2,fornecedores2,nome2,pantone_codigo2,red2,green2,blue2,float(c2),float(m2),float(y2),float(k2))
#                 st.markdown(script, unsafe_allow_html=True)
#                 st.button('proximo', key='proximo', on_click=add_count)