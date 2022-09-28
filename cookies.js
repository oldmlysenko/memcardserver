
function SetCookie(cname, cvalue, exdays=365) 
{
    //console.log("SetCookie",cname, cvalue);
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


function GetCookie(cname,defaultvalue) 
{
    const cvalue = GetCookieEx(cname,defaultvalue);
    //console.log("GetCookie",cname, cvalue);
    return cvalue;
}

function GetCookieEx(cname,defaultvalue) 
{
    
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) 
    {   var c = ca[i];
        while (c.charAt(0) == ' ') 
            c = c.substring(1);
        if (c.indexOf(name) == 0) 
            return c.substring(name.length, c.length);
    }
    return defaultvalue;
}
