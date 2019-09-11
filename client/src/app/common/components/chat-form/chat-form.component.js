/**
 * @prettier
 */
export const ChatClientComponent = {
	selector: 'chat',
	bindings: {
	},
	template: `
		<div class="chat-container container">
			<div class="chat-content">
				<ul class="chat-list">
					<li class="chat-list-item" ng-repeat="p in $ctrl.conversation">
						<small>{{ p.who }}:</small>&nbsp;&nbsp;{{ p.msg }}
					</li>
				</ul>
			</div>
			<form class="chat-form" ng-submit="$ctrl.submit($event)">
				<div class="form-group">
					<input type="text" 
						id="query" placeholder="Talk to a robot"
						autocomplete="off"
						ng-model="$ctrl.query"
						ng-keypress="$ctrl.keypressHandler($event)"
					/>
				</div>
				<button type="submit">Send</button>
			</form>
		</div>
    `,
	controller: class ChatClientComponent {
		constructor(EventEmitter) {
			'ngInject';

			this.query = '';
			this.conversation = [];

			this.EventEmitter = EventEmitter;
		}

		$onInit() {
			// this.BotService.getGreeting().then();
		}

		keypressHandler($event) {
			if ($event.which === 13) {	// ON ENTER
				$event.preventDefault();
				this.submit($event);
			}
		}

		submit($event) {
			console.log(" * Submit")
			console.log({
				'query': this.query
			})

			// All messages sent to bot should be lowercase!
			// (Best Practice)
			let lowercase_query = this.query.toLocaleLowerCase();

			// Add Query to Conversation
			this.conversation.push({
				'who': 'user',
				'msg': this.query
			});
		}

		// logoutUser() {
		// 	this.onLogout(
		// 		this.EventEmitter({
		// 			userEmail: this.user.email
		// 		})
		// 	);
		// }
	}
};
