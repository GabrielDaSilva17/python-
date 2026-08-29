from fasthtml.common import Div, H1, P

def gera(ti,sub):
    return Div(
        H1(ti),
        P(sub),
        P("hallo word!")
    )
    
