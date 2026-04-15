import torch
import torch.nn as nn
import torch.optim as optim

class MiniAVHuBERT(nn.Module):
    def __init__(
            self,
            video_dim =128,
            audio_dim =80,
            hidden_dim=256,
            num_heads=4,
            num_layers=3,
            vocab_size= 20,
            dropout=0.1,
    ):
        super().__init__()
        self.video_proj = nn.Linear(video_dim, hidden_dim)
        self.audio_proj = nn.Linear(audio_dim, hidden_dim)
        self.fusion = nn.Linear(hidden_dim*2, hidden_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model = hidden_dim,
            nhead=num_heads,
            dim_feedforward = hidden_dim*4,
            dropout=dropout,
            batch_first =True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers= num_layers)
        self.classifier =nn.Linear(hidden_dim, vocab_size)
    def forward(self, video_feat, audio_feat):
        hv = self.video_proj(video_feat)
        ha= self.audio_proj(audio_feat)
        h =torch.cat([hv,ha], dim=-1)
        h =self.fusion(h)
        z=self.transformer(h)
        logits=self.classifier(z)
        return logits
class DummyAVDatasetGenerator:
    def __init__(self, video_dim=128, audio_dim=80, vocab_size=20, device="cpu"):
        self.video_dim = video_dim
        self.audio_dim =audio_dim
        self.vocab_size = vocab_size
        self.device =device

        self.video_prototypes = torch.randn(vocab_size, video_dim, device =device)
        self.audio_prototypes =torch.randn(vocab_size, audio_dim, device=device) 
    def generate_batch(self, batch_size, seq_len, noise_std=0.20):
        targets = torch.randint(low=0,
                                high=self.vocab_size,
                                size=(batch_size, seq_len),
                                device=self.device)   
        video = self.video_prototypes[targets]+noise_std*torch.randn(
            batch_size, seq_len, self.video_dim, device =self.device
        )    
        audio = self.audio_prototypes[targets]+noise_std*torch.randn(
            batch_size, seq_len, self.audio_dim, device=self.device
        )
        return video, audio, targets
def apply_time_mask(x, mask_prob=0.30):
    B,T, D =x.shape
    mask = torch.rand(B,T, device =x.device) < mask_prob
    x_masked = x.clone()
    x_masked[mask] = 0.0
    return x_masked, mask
def train_demo():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device: ", device)
    batch_size =8
    seq_len = 40
    video_dim=128
    audio_dim =80
    hidden_dim = 256
    vocab_size =20
    num_heads = 4
    num_layers=3
    dropout=0.1
    epochs =15
    steps_per_epoch =40
    lr =1e-3
    mask_prob =0.30
    model = MiniAVHuBERT(
        video_dim=video_dim,
        audio_dim=audio_dim,
        hidden_dim=hidden_dim,
        num_heads=num_heads,
        num_layers=num_layers,
        vocab_size=vocab_size,dropout=dropout
    ).to(device)
    generator =  DummyAVDatasetGenerator(video_dim=video_dim,
                                             audio_dim=audio_dim,
                                             vocab_size=vocab_size,
                                             device=device,)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    print("\nTraining started....\n")
    for epoch in range(epochs):
        model.train()
        epoch_loss=0.0
        epoch_acc_masked=0.0
        epoch_acc_all =0.0
        for step in range(steps_per_epoch):
            video, audio, targets = generator.generate_batch(
            batch_size=batch_size,
            seq_len=seq_len,
            noise_std=0.20,
            )
            video_masked, video_mask =apply_time_mask(video, mask_prob=mask_prob)
            audio_masked, audio_mask = apply_time_mask(audio, mask_prob=mask_prob)
            mask = video_mask | audio_mask
            logits = model(video_masked, audio_masked)
            logits_flat = logits.reshape(-1, vocab_size)
            targets_flat = targets.reshape(-1)
            mask_flat = mask.reshape(-1)
            if mask_flat.sum()==0:
                continue
            masked_logits = logits_flat[mask_flat]
            masked_targets = targets_flat[mask_flat]
            loss = criterion(masked_logits, masked_targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            with torch.no_grad():
                preds = logits.argmax(dim=-1)
                acc_all = (preds==targets).float().mean().item()
                if mask.sum()>0:
                    acc_masked =(preds[mask]==targets[mask]).float().mean().item()
                else:
                    acc_masked =0.0
            epoch_loss +=loss.item()
            epoch_acc_all+= acc_all
            epoch_acc_masked+= acc_masked
        avg_loss= epoch_loss/steps_per_epoch
        avg_acc_all= epoch_acc_all/steps_per_epoch
        avg_acc_masked = epoch_acc_masked/steps_per_epoch
        print(
            f"Epoch {epoch+1:02d}/{epochs} |"
            f"Loss: { avg_loss:.4f} | "
            f"Acc(all): {avg_acc_all: .4f} | "
            f"ACC(masked): {avg_acc_masked: .4f}"
        )
    return model, generator, device
def run_inference(model, generator, device):
    model.eval()
    token_map = {i:f"T{i}" for i in range(generator.vocab_size)}
    with torch.no_grad():
        video, audio, targets = generator.generate_batch(batch_size=1,seq_len=20, noise_std=0.20)
        video_masked, video_mask = apply_time_mask(video, mask_prob=0.35)
        audio_masked, audio_mask = apply_time_mask(audio, mask_prob=0.35)
        mask = video_mask | audio_mask
        logits = model(video_masked, audio_masked)
        preds = logits.argmax(dim=-1)
    gt_ids = targets.squeeze(0).tolist()
    pred_ids = preds.squeeze(0).tolist()
    mask_list = mask.squeeze(0).tolist()

    gt_tokens = [token_map[t] for t in gt_ids]
    pred_tokens = [token_map[t] for t in pred_ids]
    print("\n" + "="*60)
    print("Inference demo")
    print("="*60)

    print("\nGround-truth token ids:")
    print(gt_ids)
    print("\nPredicted token ids:")
    print(pred_ids)
    print("\nMasked positions:")
    print(mask_list)

    print("\nGround-truth tokens:")
    print(" ".join(gt_tokens))

    print("\nPredicted Tokens:")
    print(" ".join(pred_tokens))

    print("\nPer-step view:")
    for i, (gt, pd,m) in enumerate(zip(gt_tokens, pred_tokens, mask_list)):
        flag = "MASKED" if m else "VISIBLE"
        ok = "☑️" if gt == pd else "❌"
        print(f"t={i:02d} | {flag:7s} | GT= {gt:>4s} | PRED= {pd:>4s} | {ok}")
if __name__ == "__main__":
    model, generator, device = train_demo()
    run_inference(model, generator, device)