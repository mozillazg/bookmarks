<template>
  <div id="app">
    <nav class="nav has-shadow">
      <div class="container">
        <div class="nav-left">
          <a class="nav-item is-tab is-active">Card</a>
          <a class="nav-item is-tab">Level</a>
          <a class="nav-item is-tab">Media object</a>
          <a class="nav-item is-tab">Menu</a>
          <a class="nav-item is-tab">Message</a>
          <a class="nav-item is-tab">Modal</a>
          <a class="nav-item is-tab">Nav</a>
          <a class="nav-item is-tab">Pagination</a>
          <a class="nav-item is-tab">Panel</a>
          <a class="nav-item is-tab">Tabs</a>
        </div>
      </div>
    </nav>


    <footer class="footer">
      <div class="container">
        <div class="content has-text-centered">
          <p>
            <strong>Bulma</strong> by <a href="http://jgthms.com">Jeremy Thomas</a>. The source code is licensed
            <a href="http://opensource.org/licenses/mit-license.php">MIT</a>. The website content
            is licensed <a href="http://creativecommons.org/licenses/by-nc-sa/4.0/">CC ANS 4.0</a>.
          </p>
          <p>
            <a class="icon" href="https://github.com/jgthms/bulma">
              <i class="fa fa-github"></i>
            </a>
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import Hello from './components/Hello'

export default {
  name: 'app',
  components: {
    Hello
  }
}
</script>

<style></style>
