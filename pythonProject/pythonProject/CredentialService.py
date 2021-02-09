import json


class COS:

    # ----- Call Secret Sauce Module
    def call_cos(self, domain, role, lockbox_id):

        try:
            self.domain = domain
            self.role = role
            self.lockbox_id = lockbox_id
            self.path = path
            self.key = key

            retryCount = 0
            retrycount = 0
            max_retry_count = 3
            retry = True
            while retry:
                try:
                    # for i in range(1, self.max_retry + 1):
                    # try:
                    # self.domain = domain
                    # self.role = role
                    # self.lockbox_id = lockbox_id
                    # self.path = path
                    # self.key=key

                    secrets_cos = {

                        'password': 'databases/rds-dataloader/password'
                    }

                    # iam_client = IamClient(domain=self.domain, role=self.role, lockbox_id=self.lockbox_id, verify=True)

                    iam_client = IamClient(domain=domain, role=role, lockbox_id=lockbox_id, verify=True)
                    cos_sec = iam_client.get_secret(path)[self.key]
                    return cos_sec
                    # retry = False

                    # except Exception as e:
                    # if retryCount > 3:
                    # retry = False
                    # raise Exception("Retried 3 times. Terminating")
                    # retryCount += 1

                    break
                except Exception as e:
                    # logger.error(f"Failed to delete with keys {err}")
                    retrycount += 1
                    if retrycount < max_retry_count:
                        continue
                    else:
                        raise Exception("Retried 3 times. Terminating")
                        logger.error(
                            "Retried 3 times After Max Retry"
                            f"Error: - {err}")
                        raise


        except Exception as e:
            print(e)
            logger.info('Error while accessing lockbox')
            logger.error(json.dumps(e.args))
