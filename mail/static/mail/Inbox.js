document.addEventListener('DOMContentLoaded', function () {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(null));

  //document.querySelector('#btn_new_sent').addEventListener('click', sent_eamil);
  document.querySelector('#compose-form').addEventListener('submit', (e) => sent_eamil(e));
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  if (email == null) {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
  }
  else {
    const id = email.id;
    const sender = email.sender;
    const date = email.timestamp;
    const body = email.body;
    let subject = email.subject;

    if (subject.slice(0, 3) != 'Re:') {
      subject = 'Re: ' + subject;
    }

    document.querySelector('#compose-recipients').value = sender;
    document.querySelector('#compose-subject').value = subject;
    document.querySelector('#compose-body').value = 'On ' + date + ' ' + email.sender + ' wrote: \n' + body;
  }
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  switch (mailbox) {
    case 'sent':
      console.log('Loading Sent page');
      render_emails(mailbox);
      break;
    case 'inbox':
      console.log('Loading inbox page');
      render_emails(mailbox);
      break;
    case 'archive':
      console.log('Loading archive page');
      render_emails(mailbox);
      break;
    default:
      console.log('EMOTIONAL DAMAGE!!');
  }
}

function sent_eamil(form) {

  form.preventDefault();

  const recipients = document.querySelector('#compose-recipients').value.split(",");
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  console.log("Result is:");
  console.log(recipients.toString());

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients.toString(),
      subject: subject,
      body: body
    })
  })
    .then(response => response.json())
    .then(result => {
      // Print result
      console.log(result);
    });
  // Wait until charge the sent page with the new email
  wait(400)
  load_mailbox('sent');

}

function load_email(email_id) {
  // Show the mailbox and hide other views
  const current_view = document.querySelector('#email-view');
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  current_view.style.display = 'block';

  fetch('/emails/' + email_id)
    .then(response => response.json())
    .then(email => {
      // Print email
      console.log(email);

      // ... do something else with email ...
      const id = email.id;
      const sender = email.sender;
      const arrayRecipents = email.recipients;
      const subject = email.subject;
      const body = email.body;
      const date = email.timestamp;
      const read = email.read;

      current_view.innerHTML = `<h3>From: ${sender}</h3>` + `<h3> To: ${arrayRecipents.toString()} </h3>` + `<p> Subject: ${subject}</p>` + `<p> Sent on: ${date}</p>` + `<p> Body: ${body}</p>`;

      // setting the button
      const reply_button = document.createElement('button');
      reply_button.innerHTML = "Reply";
      reply_button.classList.add('btn');
      reply_button.classList.add('btn-sm');
      reply_button.classList.add('btn-outline-primary');
      reply_button.addEventListener('click', function (event) {
        compose_email(email);
      });

      current_view.appendChild(reply_button);

      if (read == false) {
        // Updating the status to Read
        fetch('/emails/' + email_id, {
          method: 'PUT',
          body: JSON.stringify({
            read: true
          })
        })
      }
    });
}

// Support functions
function render_emails(address) {
  // Building up the macro structure to displays eamils
  const eamil_container = document.createElement('div');
  eamil_container.classList.add('container');
  document.querySelector('#emails-view').appendChild(eamil_container);

  fetch('/emails/' + address)
    .then(response => response.json())
    .then(emails => {
      // Print emails
      console.log(emails);
      // Get the email's elements
      emails.forEach(element => {
        const row_email = document.createElement('div');
        row_email.classList.add('row');

        const email_div = document.createElement('div');
        email_div.classList.add('col');
        const email_button_div = document.createElement('div');
        email_button_div.classList.add('col');

        const id = element.id;
        const sender = element.sender;
        const arrayRecipents = element.recipients;
        const subject = element.subject;
        const body = element.body;
        const date = element.timestamp;
        const read = element.read;

        // Assembly email div
        row_email.appendChild(email_div);
        eamil_container.appendChild(row_email);

        //Rendering the emails
        if (address == "inbox") {
          email_div.innerHTML = `<h3> From: ${sender} </h3>` + `<p> Subject: ${subject}</p>` + `<p> Sent on: ${date}</p>`;
          // Setting the Style CSS
          if (read) {
            row_email.classList.add('email_read_display');
          }
          else {
            row_email.classList.add('email_unread_display');
          }

          // setting the button
          const archive_button = document.createElement('button');
          archive_button.innerHTML = "Archive";
          archive_button.classList.add('btn');
          archive_button.classList.add('btn-sm');
          archive_button.classList.add('btn-outline-primary');
          archive_button.setAttribute("emial_id", id)
          archive_button.addEventListener('click', function (event) {
            archive_email(this.getAttribute("emial_id"), true);
            wait(400);//wait until the information is updated (0.5 sec)
            load_mailbox("inbox");
            event.stopPropagation();
          });
          email_button_div.appendChild(archive_button);
          row_email.appendChild(email_button_div);
        }
        else if (address == "sent") {
          email_div.innerHTML = `<h3> To: ${arrayRecipents.toString()} </h3>` + `<p> Subject: ${subject}</p>` + `<p> Sent on: ${date}</p>`;
          // Setting the Style CSS
          row_email.classList.add('email_unread_display');
        }
        else if (address == "archive") {
          email_div.innerHTML = `<h3> From: ${sender} </h3>` + `<p> Subject: ${subject}</p>` + `<p> Sent on: ${date}</p>`;
          // Setting the Style CSS
          if (read) {
            //email_div.classList.add('email_read_display');
            row_email.classList.add('email_read_display');
          }
          else {
            //email_div.classList.add('email_unread_display');
            row_email.classList.add('email_unread_display');
          }

          // seeting the button
          const archive_button = document.createElement('button');
          archive_button.innerHTML = "Un-archive";
          archive_button.classList.add('btn');
          archive_button.classList.add('btn-sm');
          archive_button.classList.add('btn-outline-primary');
          archive_button.setAttribute("emial_id", id)
          archive_button.addEventListener('click', function (event) {
            archive_email(this.getAttribute("emial_id"), false);
            wait(400);//wait until the information is updated (0.5 sec)
            load_mailbox("inbox");
            event.stopPropagation();
          });
          email_button_div.appendChild(archive_button);
          row_email.appendChild(email_button_div);
        }

        row_email.setAttribute("emial_id", id);

        // Setting an event handler
        row_email.addEventListener('click', function () {
          load_email(this.getAttribute("emial_id"));
        });
      }
      );
    })
}

function archive_email(email_id, flag) {
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
      archived: flag
    })
  })
}

function wait(ms) {
  var start = new Date().getTime();
  var end = start;
  while (end < start + ms) {
    end = new Date().getTime();
  }
}
