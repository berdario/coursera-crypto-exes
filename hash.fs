open System.Security.Cryptography
open System.Collections.Generic

let printables = [for c in List.map char ([0..127]) do if not (System.Char.IsControl(c)) then yield c]

let rec product xss =
    match xss with
    | [] -> Seq.singleton []
    | (xs::yss) -> seq{for p in (product yss) do for x in xs do yield x::p }

let words = Seq.initInfinite (fun i -> List.replicate i printables |> product) |> Seq.concat |> Seq.map (fun x -> System.String.Join("", x))

let results = new Dictionary<byte list, byte[]>()

let pick_collision (i, (bytes, hash)) =
    if results.ContainsKey hash then
        Some(bytes, hash, results.[hash])
    else
        do
            ignore (results.Add(hash, bytes))
            if i%1000000 = 0 && i>0 then do
                //printfn "%A" i
                System.Environment.Exit 0
        None

let flag x = (log (float x) / log 2.0 + 1.0 |> int |> pown 2 )-1

let padded_byte x wbyte =
    if x>0 then
        [|byte (flag x) &&& wbyte|]
    else
        [||]

let last_bits n (bytes: byte[]) =
    let l = bytes.Length
    let n_bytes = n/8
    let rem = n%8
    let wbyte = padded_byte rem bytes.[l-n_bytes-1]
    bytes.[l-n_bytes..] |> Array.append wbyte |> Array.toList

let find_collisions =
    let sha256 = new SHA256Managed()
    let encoding = new System.Text.ASCIIEncoding()
    let bytes = seq{for word in words -> encoding.GetBytes word}
    let hashes : seq<(int*(byte[]*byte list))> = seq{for bs in bytes -> bs, sha256.ComputeHash bs |> last_bits 40}|>Seq.zip (Seq.initInfinite id)
    let collision = Seq.pick pick_collision hashes
    let (first, hash, second) = collision
    encoding.GetString(first), encoding.GetString(second), hash

let main =
    printfn "%A" find_collisions

(*
how does this actually work? why the monadic "let!" ?

type Product () =
  member this.Bind (l,f) = List.collect f l
  member this.Return n = [n]

let enumeratedPizzas =
  Product() {
    let! x = ["New York";"Chicago"]
    let! y = ["Pepperoni";"Sausage"]
    let! z = ["Cheese";"Double Cheese"]
    return x,y,z
  }

*)