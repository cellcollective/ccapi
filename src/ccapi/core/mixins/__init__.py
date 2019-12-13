class JupyterHTMLViewMixin(object):
    def _repr_html_(self):
        attrs = sorted(filter(lambda a: not (a.startswith("_") or callable(a)),
            dir(self)))
        body  = ""

        for attr in attrs:
            body += """
                <tr>
                    <td>
                        <strong>
                            {name}
                        </strong>
                    </td>
                    <td>
                        {value}
                    </td>
                </tr>
            """.format(name = attr, value = getattr(self, attr, None))

        template = """
            <table>
                {body}
            </table>
        """.format(body = body)

        return template