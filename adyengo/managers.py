from django.db import models, IntegrityError
from . import api
from . import constants


class RecurringContractManager(models.Manager):

    def contracts(self, shopper_reference, contract_type):
        """
        Returns a list of Recurring Payment Contracts.

        It firsts looks in the "cache" (database), if it can't find any
        records, it will use `_fetch_contracts()` which will fetch the
        contracts from the Adyen API.
        """

        contracts = self.filter(
            shopper_reference=shopper_reference,
            contract_type=contract_type
        )

        if contracts.count():
            return contracts
        else:
            return self._fetch_contracts(shopper_reference, contract_type)

    def flush_cache(self, shopper_reference, contract_type):
        """
        Flushes the Recurring Payment Contracts cache.

        This will ensure that the next time `contracts()` is executed, it won't
        find any contracts in the cache and will do a request to the Adyen API
        (and will refill the cache).
        """
        try:
            self.filter(
                shopper_reference=shopper_reference,
                contract_type=contract_type
            ).delete()
        except:
            pass

    def _fetch_contracts(self, shopper_reference, contract_type):
        """
        Will fetch the Recurring Payment Contracts from the Adyen API, save
        them to the database and return the list of `RecurringContract` models.

        If there are no Recurring Payment Contracts, it won't save anything to
        the database and will return an empty list.
        """

        result = api.list_recurring_details(shopper_reference, contract_type)

        if 'details' in result:
            return self._save_contracts(shopper_reference, contract_type, result)
        else:
            return []

    def _save_contracts(self, shopper_reference, contract_type, result):
        """
        Saves the contracts returned from the Adyen API to the database and
        returns the list of `RecurringContract` models.
        """

        contracts = []

        for contract in result.get('details'):

            detail = contract.get('RecurringDetail')

            if not detail:
                continue

            # Adyen is too retarded to tell us what payment method type it is
            # so we'll have to find out for ourselves by checking which one is
            # filled...

            def get_payment_method_type():
                for t in ('card', 'elv', 'bank'):
                    if t in detail:
                        return t

            payment_method_type = get_payment_method_type()

            contract = self.model(
                shopper_reference=shopper_reference,
                contract_type=contract_type,
                recurring_detail_reference=detail.get('recurringDetailReference'),
                variant=detail.get('variant'),
                payment_method_type=payment_method_type,
                creation_date=detail.get('creationDate')
            )

            try:
                contract.save()
            except IntegrityError:
                # Because of race conditions, it is possible that the contract
                # already exists. If so, the model will throw an
                # `IntegrityError`. In this case we'll skip inserting this
                # contract because we already have it.
                continue

            # Each payment method type has different fields, we save these in
            # the `RecurringContractDetail` objects that have foreign keys
            # to `RecurringContract`.

            fields = detail[payment_method_type]

            for fieldname in constants.RECURRING_CONTRACT_VARIANT_FIELDS[payment_method_type]:

                if fieldname in fields:
                    contract.details.create(
                        recurring_contract=contract,
                        key=fieldname,
                        value=fields[fieldname]
                    )

            contracts.append(contract)

        return contracts
