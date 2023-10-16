import numpy as np
import plotly.colors as c
import plotly.graph_objects as go

from blockops import BlockProblem


def fine_discretization_error(N, tEnd, M, scheme, points, quadType, form,
                              reLambdaLow, reLambdaHigh, imLambdaLow,
                              imLambdaHigh, nVals, eMin, eMax):

    reLam = np.linspace(reLambdaLow, reLambdaHigh, nVals)
    imLam = np.linspace(imLambdaLow, imLambdaHigh, nVals)

    lam = reLam[:, None] + 1j * imLam[None, :]
    prob = BlockProblem(lam.ravel(),
                        tEnd=tEnd,
                        nBlocks=N,
                        nPoints=M,
                        scheme=scheme,
                        points=points,
                        quadType=quadType,
                        collUpdate=False)

    uExact = prob.getSolution('exact')
    uNum = prob.getSolution('fine')
    err = np.abs(uExact - uNum)
    err = np.max(err, axis=(0, -1)).reshape(lam.shape)

    err = err.transpose()
    log_err = np.log(err)

    err[err < 10**eMin] = 10**eMin
    err[err > 10**eMax] = 10**eMax
    ticks = [10**(i) for i in range(eMin, eMax + 1)]

    color_names = [
        f'{tick:.0e}' if tick != 1.0 else f'{tick}' for tick in ticks
    ]
    color_vals = np.linspace(
        np.min(log_err) - .5,
        np.max(log_err) + .5, len(color_names))

    fig = go.Figure(data=go.Contour(z=log_err,
                                    x=reLam.ravel(),
                                    y=imLam.ravel(),
                                    colorscale=c.sequential.Sunset,
                                    colorbar=dict(tickvals=color_vals,
                                                  ticktext=color_names),
                                    hovertext=err,
                                    hoverinfo='x+y+text'))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig.to_json()


def compute_plot():
    fig = go.Figure(data=go.Contour(
        z=[[10, 10.625, 12.5, 15.625, 20], [5.625, 6.25, 8.125, 11.25, 15.625],
           [2.5, 3.125, 5., 8.125, 12.5], [0.625, 1.25, 3.125, 6.25, 10.625],
           [0, 0.625, 2.5, 5.625, 10]],
        colorscale='Electric',
    ))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    return fig.to_json()
