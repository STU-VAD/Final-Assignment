from load_data import load_co2_data, load_temperature_data, save_json
import json

def main():
    # Load data
    co2_data = load_co2_data('../../data/co2_annmean_gl.csv')
    temp_data = load_temperature_data('../../data/ZonAnn.Ts+dSST.csv')

    # Create combined data
    combined_data = {
        'years': co2_data['years'],
        'data': []
    }

    for i, year in enumerate(co2_data['years']):
        year_data = {
            'year': year,
            'co2': co2_data['mean'][i],
            'co2Unc': co2_data['unc'][i],
            'temperatures': {}
        }

        # Find temperature data for this year
        if year in temp_data['years']:
            year_idx = temp_data['years'].index(year)
            for j, band in enumerate(temp_data['latitudeBands']):
                year_data['temperatures'][band] = temp_data['anomalies'][year_idx][j]

        combined_data['data'].append(year_data)

    # Save JSON files
    save_json(co2_data, '../observable/public/data/co2.json')
    save_json(temp_data, '../observable/public/data/temperature.json')
    save_json(combined_data, '../observable/public/data/combined.json')

    print("Data preprocessing complete!")

if __name__ == '__main__':
    main()
