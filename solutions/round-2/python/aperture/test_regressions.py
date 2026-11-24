from orchestration.models import JobStatus
from orchestration.service import OrchestrationService


def test_apt410_dequeue_does_not_redeliver_same_job():
    svc = OrchestrationService()
    svc.enqueue("a")

    assert svc.dequeue() == "a"
    assert svc.dequeue() is None


def test_apt415_acked_job_is_not_redelivered():
    svc = OrchestrationService()
    svc.enqueue("a")

    assert svc.dequeue() == "a"
    svc.ack("a")

    assert svc.dequeue() is None
    assert svc.registry.status("a") is JobStatus.DONE


def test_apt415_ack_alone_takes_queued_job_out_of_circulation():
    # Isolated from the dequeue defect: ack must be sufficient on its own.
    svc = OrchestrationService()
    svc.enqueue("a")

    svc.ack("a")

    assert svc.dequeue() is None


def test_apt421_dead_letters_on_first_nack_when_max_retries_is_one():
    svc = OrchestrationService(max_retries=1)
    svc.enqueue("a")
    svc.dequeue()

    svc.nack("a")

    assert svc.dead_letters() == ["a"]
    assert svc.registry.status("a") is JobStatus.DEAD


def test_apt421_dead_letters_on_second_nack_when_max_retries_is_two():
    svc = OrchestrationService(max_retries=2)
    svc.enqueue("a")
    svc.dequeue()

    svc.nack("a")
    assert svc.registry.status("a") is JobStatus.READY
    assert svc.dequeue() == "a"

    svc.nack("a")
    assert svc.dead_letters() == ["a"]
    assert svc.registry.status("a") is JobStatus.DEAD


if __name__ == "__main__":
    tests = [
        test_apt410_dequeue_does_not_redeliver_same_job,
        test_apt415_acked_job_is_not_redelivered,
        test_apt415_ack_alone_takes_queued_job_out_of_circulation,
        test_apt421_dead_letters_on_first_nack_when_max_retries_is_one,
        test_apt421_dead_letters_on_second_nack_when_max_retries_is_two,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
