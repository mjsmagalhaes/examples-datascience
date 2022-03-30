import jp from 'jsonpath';
import jsonata from 'jsonata';
import * as R from 'ramda';

export const filter = R.curry((query_string, json_data) => jp.query(json_data, query_string));

export const transform = R.curry((query_string, json_data) => jsonata(query_string).evaluate(json_data));