import sbk_scraping.parser.common as cmn
from pydantic import conlist


class JsonParser(cmn.BaseModel, cmn.HttpResponseParser):

    json_document: dict
    srch_list_expressions: conlist(cmn.SearchExpression, min_items=1)

    def parse(self) -> dict:
        import jmespath
        result = {}

        for qry_expression in self.srch_list_expressions:
            qry_result = jmespath.search(
                expression=qry_expression.srchex,
                data=self.json_document
            )
            if qry_result in ('', None, []):
                continue

            result[qry_expression.target_id] = qry_result

        return result
