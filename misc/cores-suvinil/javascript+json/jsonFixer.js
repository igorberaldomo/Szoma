import pant from 'nearest-pantone'
import data from './pantone-colors.json' with {type: 'json'}
import fs from 'fs'
var List = {}
let values = data['values']
let tamanho = (data['values'].length)
let c =0
while (c < tamanho){
    let json = pant.getClosestColor(values[c])
    List[values[c]] = json
    c++
}
const newJson = fs.writeFileSync('pantone.json', JSON.stringify(List))