# dataset settings
data_keys = ['motion', 'motion_mask', 'motion_length', 'clip_feat', 'sample_idx', 'text_idx', 'specified_idx', 'stickman_tracks', 'norm_joints'] 
meta_keys = ['text', 'token']
crop_size = 196
train_pipeline = [
    dict(type='Crop', crop_size=crop_size),
    dict(
        type='Normalize',
        mean_path='data/datasets/kit_ml/mean.npy',
        std_path='data/datasets/kit_ml/std.npy'),
    dict(type='ToTensor', keys=data_keys),
    dict(type='Collect', keys=data_keys, meta_keys=meta_keys)
]

data = dict(
    samples_per_gpu=256,
    workers_per_gpu=20,
    train=dict(
        type='RepeatDataset',
        dataset=dict(
            type='Stickmant2mDataset',
            dataset_name='kit_ml',
            data_prefix='data',
            pipeline=train_pipeline,
            ann_file='train.txt',
            motion_dir='motions',
            text_dir='texts',
            token_dir='tokens',
            clip_feat_dir='clip_feats',
            crop_size=crop_size
        ),
        times=100
    ),
    test=dict(
        type='Stickmant2mDataset',
        dataset_name='kit_ml',
        data_prefix='data',
        pipeline=train_pipeline,
        ann_file='test.txt',
        motion_dir='motions',
        text_dir='texts',
        token_dir='tokens',
        clip_feat_dir='clip_feats',
        crop_size=crop_size,
        eval_cfg=dict(
            shuffle_indexes=True,
            replication_times=2,
            replication_reduction='statistics',
            text_encoder_name='kit_ml',
            text_encoder_path='data/evaluators/kit_ml/finest.tar',
            motion_encoder_name='kit_ml',
            motion_encoder_path='data/evaluators/kit_ml/finest.tar',
            metrics=[
                dict(type='R Precision', batch_size=32, top_k=3),
                dict(type='Matching Score', batch_size=32),
                dict(type='FID'),
                dict(type='Diversity', num_samples=300),
                dict(type='MultiModality', num_samples=50, num_repeats=30, num_picks=10)
            ]
        ),
        test_mode=True
    )
)