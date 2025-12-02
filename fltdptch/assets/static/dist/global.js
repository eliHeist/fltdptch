
// request methods

// get csrf from dom
function csrf() {
    // 1. Try to get the token from cookies (most common for AJAX)
    const cookieName = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.startsWith(cookieName + '=')) {
            return cookie.substring(cookieName.length + 1);
        }
    }

    // 2. If not found in cookies, try to get it from a hidden input field
    //    This is useful if the token is only rendered in the HTML, e.g., via {% csrf_token %}
    const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (csrfInput && csrfInput.value) {
        return csrfInput.value;
    }

    // If token is not found in either place
    console.warn("CSRF token not found. Ensure {% csrf_token %} is used in your template or the 'csrftoken' cookie is set.");
    return null;
}
async function GET(url, return_full=false) {
    const response = await fetch(url);
    if (return_full) {
        return response
    }
    return await response.json();
}
async function POST(url, obj, return_full=false) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
        },
        body: JSON.stringify(obj)
    });
    if (return_full) {
        return response
    }
    return await response.json();
}
async function PUT(url, obj, return_full=false) {
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
        },
        body: JSON.stringify(obj)
    });
    if (return_full) {
        return response
    }
    return await response.json();
}
async function DELETE(url, obj = null, return_full=false) {
    let body = ''
    if (obj) {
        body = JSON.stringify(obj)
    }
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
        },
        body: body
    });
    if (return_full) {
        return response
    }
    return await response.json();
}

async function PATCH(url, obj, return_full=false) {
    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf(),
        },
        body: JSON.stringify(obj)
    });
    if (return_full) {
        return response;
    }
    return await response.json();
}

function callyChange(id) {
    // console.log('callyChange', id);
    const cally = document.querySelector(id);
    let date = cally.value;
    const selector = cally.getAttribute('target-element')
    const target_input = document.querySelector(selector);

    if (target_input) {
        target_input.value = date;
        // Trigger an input event to notify any listeners
        const event = new Event('input', { bubbles: true });
        target_input.dispatchEvent(event);
    }
}
