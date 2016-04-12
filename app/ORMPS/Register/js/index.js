var working = false;
$('.register').on('submit', function(e) {
  e.preventDefault();
  if (working) return;
  working = true;
  var $this = $(this),
  $state = $this.find('button > .state');
  $this.addClass('loading');
  $state.html('Registering');
  setTimeout(function() {
    $this.addClass('ok');
    $state.html('Welcome to the Online Meal Planner and Recipe System!');
    setTimeout(function() {
      $state.html('Register');
      $this.removeClass('ok loading');
      working = false;
    }, 4000);
  }, 3000);
});