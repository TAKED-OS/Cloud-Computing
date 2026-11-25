<?php

function publish_capsule_sealed(array $capsule): void
{
    $topic = config('CAPSULE_EVENTS_TOPIC_ARN');
    if ($topic === null) {
        throw new RuntimeException('CAPSULE_EVENTS_TOPIC_ARN is required.');
    }

    $id = (int) $capsule['id'];
    $client = new Aws\Sns\SnsClient(['region' => config('AWS_REGION', 'eu-central-1')]);
    $client->publish([
        'TopicArn' => $topic,
        'Message' => json_encode([
            'type' => 'capsule.sealed',
            'version' => 1,
            'event_id' => 'capsule.sealed:' . $id,
            'occurred_at' => gmdate('Y-m-d\TH:i:s\Z'),
            'capsule_id' => $id,
        ], JSON_THROW_ON_ERROR),
    ]);
}
