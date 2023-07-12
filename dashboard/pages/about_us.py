from dash import  html

#layout to serve the about_us path where is the information about our team
layout = html.Div([        
        html.Div([
            html.A([html.H1("Alexander Mosquera Perdomo"),html.Img(src='/assets/img/alex.jpg',className='card-image'),
            html.P("Electronic and telecommunications engineering student, data analyst and enthusiast of sustainable development entrepreneurships.\
                 I am curious, responsible, comitted and passionate about learning and innovation. Experienced in development of academic and resesearch\
                     projects supported on the flow of data that involve fields of AI and knowledge managment.", style={'height':'16rem'})], 
            className='card card-body',href='https://www.linkedin.com/in/alexander-mosquera-perdomo-a08364231/')
        ], className='col-1'),
        html.Div([
            html.A([html.H1("Jarby Daniel Salazar Galindez"),html.Img(src='/assets/img/hugo_r.jpg',className='card-image'),
            html.P("Electronic and telecommunications engineering student, data analyst and enthusiast of sustainable development entrepreneurships.\
                 I am curious, responsible, comitted and passionate about learning and innovation. Experienced in development of academic and resesearch\
                     projects supported on the flow of data that involve fields of AI and knowledge managment.", style={'height':'16rem'})], 
            className='card card-body',href='https://www.linkedin.com/in/alexander-mosquera-perdomo-a08364231/')
        ], className='col-1'),
], className='row top')