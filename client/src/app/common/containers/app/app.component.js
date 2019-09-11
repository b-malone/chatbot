export const AppComponent = {
  selector: 'app',
  template: `
    <div class="app">
      <chat></chat>
    </div>
  `,
  controller: class AppComponent {
    constructor() {
      'ngInject';

      this.button = null;
      this.user = {};
    }

    // $onInit() {}
    // <app-nav
    //     user="$ctrl.user"
    //     on-logout="$ctrl.logout($event);"
    //     button-title="{{$ctrl.button}}">
    //   </app-nav>
  }
};
