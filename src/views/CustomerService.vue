<template>
    <section class="mb-4">
    <br><br><br><h2>Contact Us</h2><br>
    <div class="block">
        <p class="text-center w-responsive mx-auto mb-5" ><em>For any questions or concerns do not hesitate to contact us directly</em></p>
        <form id="contact-form" name="contact-form" action="mail.php" method="POST">
            <label for="name" class=""><b>Your name</b></label>
            <input type="text" id="name" name="name" class="form-control">
            <label for="email" class=""><b>Your email</b></label>
            <input type="text" id="email" name="email" class="form-control">
            <label for="subject" class=""><b>Subject</b></label>
            <input type="text" id="subject" name="subject" class="form-control">
            <label for="message"><b>Your message</b></label>
            <textarea type="text" id="message" name="message" rows="2" class="form-control md-textarea"></textarea>
        </form><br><br>
        <a class="btn btn-primary" onclick="document.getElementById('contact-form').submit();">Submit</a>
    </div><br><br><br>
        <ul class="list-unstyled mb-0">
            <li><i class="fas fa-map-marker-alt fa-2x"></i>
                <p>Montreal, Canada</p>
            </li>
            <li><i class="fas fa-phone mt-4 fa-2x"></i>
                <p>438-888-0000</p>
            </li>
            <li><i class="fas fa-envelope mt-4 fa-2x"></i>
                <p>354thestars@shop.com</p>
            </li>
        </ul>
    </section>
</template>

<script>
export default{
  name: 'CustomerService'
}
</script>

<style lang="scss" scoped>

.block{
  background-color:#dbedff;
  border:1px;
  border-style:solid;
  border-color:#0e0e3f;
  padding:1em;
  display:inline-block;
  width:900px;
  height:500px;
}
</style>
