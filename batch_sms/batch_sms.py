import dataset

class BatchSMS:
    def __init__(self, db_file, batch_sender):
        self.db = dataset.connect('sqlite:///%s' % db_file)
        self.batch_sender = batch_sender

        # prepare db
        self.from_numbers = self.db.get_table('from_numbers', primary_id='number', primary_type='String')
        self.to_numbers = self.db.get_table('to_numbers', primary_id='number', primary_type='String')
        self.associations = self.db.get_table('associations', primary_id='to_num', primary_type='String')
        self.subscription_lists = self.db.get_table('subscription_lists')
        self.subscriptions = self.db.get_table('subscriptions')

    # From Numbers
    def add_from_number(self, from_num):
        self.from_numbers.upsert(dict(number=from_num), ['number'])

    def remove_from_number(self, from_num):
        self.from_numbers.delete(number=from_num)

    # To Numbers
    def add_to_number(self, to_num):
        self.to_numbers.upsert(dict(number=to_num), ['number'])

    def remove_to_number(self, to_num):
        self.to_numbers.delete(number=to_num)

    def associate(self, to_num, from_num):
        # these should both be foreign keys, but too lazy to use ORM
        self.associations.upsert(dict(to_num=to_num, from_num=from_num), ['to_num'])

    # Subscription Lists
    def create_subscription_list(self, name):
        # TODO: ensure this returns id
        return self.subscription_lists.insert({'name': name})

    def update_subscription_list(self, subscription_id, name):
        self.subscription_lists.update({'id': subscription_id, 'name': name}, ['id'])

    def get_subscription_lists_by_name(self, name):
        return self.subscription_lists.find(name=name)

    # Subscriptions
    def add_to_subscription(self, to_num, subscription_id):
        # subscription should be a foreign key,
        # but I'm too lazy to use a full-blown ORM for this
        self.subscriptions.insert({'to_num': to_num, 'subscription': subscription_id})