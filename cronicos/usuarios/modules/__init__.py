def html_Dotacion(num, day):    
    day = str(day)

    if num == 0: 
        return '<span class="w3-tag w3-sand"> <i class="fa fa-exchange"></i> / '+ day + '</span>'
    
    elif num == 1:
        return '<span class="w3-tag w3-pale-blue"> I - ' + day + '</span>'
    
    elif num == 2: 
        return '<span class="w3-tag w3-pale-blue"> II - ' + day + '</span>'

    else: 
        return '<span class="w3-tag w3-pale-blue"> III - ' + day + '</span>'
              
        

    







