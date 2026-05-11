import torch

NEF_INF = torch.finfo(torch.float32).min
def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank =0, reduction="none"):
    # ex: targetss [28,1,17,21]
    # log_probs.shape-> (T X BX C)
    #input_lengths.shape  ->(B,)
    #target_lengths.shape->(B,)
    seq_len, batch_size, num_classes = log_probs.shape
    B = torch.arange(batch_size)
    # _t_a_r_g_e_t_s_:[28,1,17,21,0] -> Append a blank token at the end (we could really use anything, doent matter)
    # its just a placeholder so our indexing is happy , we will never this token anywhere or include it in the loss
    _t_a_r_g_e_t_s_ = torch.cat([targets, torch.zeros(batch_size, 1, device = log_probs.device, dtype=torch.long)], dim=-1)
    #print(_t_a_r_g_e_t_s_)
    # _t_a_r_g_e_t_s_ : [0,28,0,1,0,17,0,21,0,0]-> Insert blank tokens in between targets
    _t_a_r_g_e_t_s_ = torch.stack([torch.full_like(_t_a_r_g_e_t_s_, blank), _t_a_r_g_e_t_s_], dim =-1).flatten(start_dim=-2)
    diff_labels = (_t_a_r_g_e_t_s_[:, :-2] != _t_a_r_g_e_t_s_[:,2:])
    print(diff_labels.shape, _t_a_r_g_e_t_s_.shape)

if __name__ =="__main__":
    T, B, C = 128, 2, 32
    t =50
    blank =0 
    device = "cuda" if torch.cuda.is_available() else "cpu"

    logits = torch.randn(T,B, C).requires_grad_().to(device)
    log_probs =logits.log_softmax(dim =-1).to(device)
    targets = torch.randint(1,C,(B,t), dtype=torch.long).to(device)
    input_lengths = torch.full((B,),T, dtype=torch.long).to(device)
    target_lengths =torch.full((B,), t, dtype=torch.long).to(device)
    ctc_loss(log_probs= log_probs, targets=targets, input_lengths= input_lengths, target_lengths= target_lengths)

