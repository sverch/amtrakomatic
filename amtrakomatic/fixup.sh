echo '[]' >| test_data/seattle_chicago_08_24_2019_False_0.json 
echo '[]' >| test_data/boston_newyork_08_24_2019_False_2.json 
echo '[]' >| test_data/boston_newyork_08_24_2019_False_1.json 
echo '[]' >| test_data/Boston_vermont_08_18_2019_False_0.json
bash extract_expected_result.sh >| temp.json
mv temp.json test_data/boston_newyork_08_24_2019_False_1.json 
bash extract_expected_result.sh >| temp.json
mv temp.json test_data/boston_newyork_08_24_2019_False_2.json 
bash extract_expected_result.sh >| temp.json
mv temp.json test_data/Boston_vermont_08_18_2019_False_0.json
echo '[]' >| test_data/Boston_vermont_08_18_2019_False_0.json
bash extract_expected_result.sh >| temp.json
mv temp.json test_data/seattle_chicago_08_24_2019_False_0.json 
